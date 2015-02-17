'''
Runs CoreNLP sentiment pipeline on csv file containing at least columns 'PhraseId' and 'Phrase'
Outputs probabilities computed by Stanford RNN and overall sentiment from 0 to 4 in csv format
If output files already exists, will suggest appending

Requirements:
    - download all *.jar files from CoreNLP sentiment page: http://search.maven.org/#browse%7C304784840
    - download matrix library file ejml-0.23.jar from https://code.google.com/p/efficient-java-matrix-library/downloads/detail?name=ejml-0.23.jar&can=2&q=
    - put everything in the same directory
    - run this script from this directory

Command line:
    $ python runCoreNLPSentiment.py train.tsv train_labels.txt
'''
import pexpect,sys
import os
import time
class coreNLPsentiment:
    javacommand = 'java -cp \"*\" -mx5g edu.stanford.nlp.sentiment.SentimentPipeline -output PROBABILITIES,ROOT -stdin'
    labels={'Very positive':4, 'Positive':3,'Neutral':2,'Negative':1,'Very negative':0}

    def __init__(self):

        #start process
        self.proc = pexpect.spawn(self.javacommand)

        #wait for process ready
        print 'Java process started, waiting for it to be ready...'
        readyMsg = 'Processing will end when EOF is reached.'
        self.proc.expect(readyMsg)

    def processLine(self, phrase, linenb, phraseid):
        verbose = (linenb%100==0)
        #verbose = True

        #send to corenlp
        if verbose: print 'sending line to CoreNLP java process, line nb=%d, phraseid=%d, line=%s'%(linenb,phraseid,phrase)
        self.proc.sendline(phrase)

        errormsg = None
        #wait for probabilities
        try:
            self.proc.expect('0:(  [0-1]\.[0-9]{4}){5}',timeout=10)
            #interpret output
            out=self.proc.after
            if verbose: print 'before=',self.proc.before
            if verbose: print 'after=',self.proc.after
            probas = [float(x) for x in out.split('  ')[1:]]
            if verbose: print 'received probabilities: %s'%probas
        except pexpect.TIMEOUT:
            errormsg = 'no recognized probas received for line nb=%d, phraseid=%d, phrase=%s. defaulting to uniform'%(linenb,phraseid,phrase)
            probas = [0.2]*5

        #wait for overall sentiment (should be max of probas)
        try:
            self.proc.expect(self.labels.keys(),timeout=10)
            #interpret output
            out=self.proc.after
            sentiment = self.labels[out]
            if verbose:print 'received sentiment: %s'%out
        except pexpect.TIMEOUT:
            errormsg = 'no recognized sentiment received for line nb=%d, phraseid=%d, phrase=%s. defaulting to 2'%(linenb,phraseid,phrase)
            sentiment = 2

        return probas,sentiment,errormsg

fileinpath = sys.argv[1]
fileoutpath = sys.argv[2]

#check if out file already exists and ask if append or overwrite
if os.path.isfile(fileoutpath):
    readmode = ''
    while not(readmode in ['a','w']): 
        print 'Output file %s already exists. (w)riteover, (a)ppend ?'%fileoutpath
        readmode = raw_input() 
else:
    readmode = 'w'

print 'Processing input file %s, output to file %s,readmode=%s'%(fileinpath,fileoutpath,readmode)

#read output file if existing to figure out which lines to skip
#startAtPhraseId=18500
startAtPhraseId=-1

if readmode == 'a':
    print 'Checking lines already in output file...'
    with open(fileoutpath,'r') as fileoutread:
        for line in fileoutread:
            pass
        last = line
        print 'Last line in output file is %s'%line
        lastPhraseId=int(last.split(',')[0])
        print 'Last phrase id in output file is %d. Ignoring everything before.'%lastPhraseId
        startAtPhraseId = lastPhraseId

print 'Starting CoreNLP java process'
corenlp = coreNLPsentiment()

previousTime = time.time()
print 'Java process ready, opening files for input/output and start sentiment analysis'
with open(fileinpath,'r') as filein:
    with open(fileoutpath,readmode) as fileout:
        headers = filein.readline().rstrip('\n').split('\t')
        i = 0
        errors = []
        #write headers to output file
        if readmode == 'w':
            fileout.write('PhraseID,Sentiment,'+','.join(['proba%d'%k for k in range(1,6)])+'\n')

        #start processing lines
        for line in filein:
            i += 1
            verbose= (i % 100 == 0)

            #timing
            if verbose:
                currentTime=time.time()
                elapsedMs = (currentTime-previousTime)*1000.0
                previousTime=currentTime
                print 'Current speed=%f ms/line'%(elapsedMs/100) 

            #read line from input file
            line = line.rstrip('\n')
            lines=dict(zip(headers,line.split('\t')))

            #get sentence
            #print lines
            phrase= lines['Phrase']
            phraseid = int(lines['PhraseId'])

            #skip already processed if necessary
            if phraseid<=startAtPhraseId:
                print 'Skipping phraseid=%d because we start after %d'%(phraseid, startAtPhraseId) 
                continue

            #fix phrases with multiple '?,!,.'
            #ellipses are treated correctly
            #hide all ellipses
            phrase = phrase.replace('...','<ellipses>')
            eolSymbs = ['.','?','!']
            total = sum([phrase.count(s) for s in eolSymbs])
            if total>1:
                for s in eolSymbs:
                    phrase = phrase.replace(s,' ')
            #put back ellipses
            phrase = phrase.replace('<ellipses>','...')

            probas,sentiment,errormsg = corenlp.processLine(phrase,i,phraseid) 

            if errormsg:
                errors.append(errormsg)
                print errormsg 

            #write to output file
            towrite = [phraseid,sentiment]+probas
            fileout.write(','.join(map(str,towrite))+'\n')

print 'Done. Processed %d lines from file %s, skipped all phraseids before %d, output to file %s, encountered errors on %d lines. Showing all errors again:'%(i, fileinpath,startAtPhraseId, fileoutpath, len(errors)/2)

for errormsg in errors:
    print errors
