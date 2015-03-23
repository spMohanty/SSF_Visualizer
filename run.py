from flask import Flask, render_template, request, redirect
import json
import SSF
import uuid
import os
from lxml import etree

app = Flask(__name__)

def getXMLofFirstSentence(d):
    for node in d.nodeList:
        if isinstance(node,SSF.Sentence):
            return node.getXML()
            break
        if not isinstance(node,SSF.Node):
            getXMLofFirstSentence(node)

@app.route("/", methods=['POST', 'GET'])
def hello():
    if request.method == 'POST':
      sentence = request.form['sentence']
      ##Write to file
      tempFileName = "tmp/"+str(uuid.uuid4().get_hex().upper()[0:6])+".tmp"
      f = open(tempFileName, "w")
      f.write(sentence)
      f.close()
      document = SSF.Document(tempFileName)
      os.remove(tempFileName)
      return render_template('index.html', sentence=getXMLofFirstSentence(document), raw_sentence=sentence)
    else:
      return render_template('index.html')

if __name__ == "__main__":
    app.debug = True
    app.run()