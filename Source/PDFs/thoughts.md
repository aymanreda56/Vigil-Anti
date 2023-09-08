* pdfsize when pdfsize == -1 is somewhat indicative for a malicious file, we cannot just drop those rows having pdfsize == -1
* same with embedded files, metadata size, pages, xref Length, title characters, isEncrypted, embedded files, stream, trailer, encrypt, ObjStm, Colors,  obj, endobj column
* I cleansed header values, by the regex "^\\tPDF-\d\.\d$"
* I added a new column "PDF_version"
* any invalid values will just be replaced by -1
* encrypt column has erroneous values, but I mapped them to -1




### the categorial Columns are:
* isEncrypted (0 or 1 or -1)
* embedded files (0 or 1 or -1)
* text ('No' or 'Yes' or 'unclear' or '-1' or '0'), 0 are erroneous
* header (contains erroneous values, deleted this column and replaced it with header_regex_boolean and PDF_Version)
* encrypt (0 or 1 or -1) erroneous values are mapped to -1
* OpenAction (0 or 1 or -1, contains -1 and is cleansed of invalid entries)
* RichMedia
* launch (0 or 1 or -1)
* XFA (0 or 1 or -1)            --> XML Form Architecture, they are just forms same as login forms
* header_regex_boolean  --> newly added column replacing the header column
* PDF_Version     --> newly added column replacing the header column
* Class (malicious or benign ---> encoded to 1 and 0)


### the numerical Columns are:
* pdfsize (contains -1)
* metadata size (contains -1)
* pages (contains -1)
* xref Length (contains -1)
* title characters (contains -1)
* images (contains -1)
* obj (contains -1)
* endobj (contains -1)
* stream (contains -1)
* endstream (contains -1)
* xref (contains -1)
* startxref (contains -1)
* trailer (contains -1)
* pageno (contains -1)
* ObjStm (contains -1)                                                --> Object Stream, array of objects but compressed together
* JS (contains -1 and is cleansed of invalid entries)
* Javascript (contains -1 and is cleansed of invalid entries)
* AA (contains -1 and is cleansed of invalid entries)                 --> additional actions
* Acroform (contains -1 and is cleansed of invalid entries)           --> interactive forms
* JBIG2Decode                                                --> "JBIG2Decode" refers to a specific filter or compression method used for image data within a PDF file. JBIG2 (Joint Bi-level Image Group) is an image compression standard designed specifically for bi-level (black and white) images.
* EmbeddedFile                         --> number of embedded files inside the PDF
* Colors




### I then performed some type castings, some columns were float, I then converted them to integers



### I am now confused whether to drop the -1 values or decide to leave them

### If I decided to leave those -1 values, I must then consider all the numeric columns as categorical or else, the -1 will lose its meaning.



### Ok, I will try:
* dumbo bumbo: use numerics as numerics, use categories as categories, the -1 values are just normal values among others
* scientific sonic: drop all the -1 entries and continue dumbo bumbo
* maniac insomniac: all columns are considered categorical so that the -1 value is preserved as a meaningful category




## dumbo bumbo:
#### WTF I tried the standard scaler and found negative values everywhere!!!!!    the -1 entries are destroying other numbers
#### ok ok, we are dumbo bumbo, let's just keep cooking
#### Try encoding categorical values
#### Give it a SVC with linear kernel and default C=1
## OMG 93% f1 score !!! HOW TF?!?
#### Try same model with C = 0.1
## 95% f1 score
#### Try same model with C=0.5
## 94%
#### Try C = 0.08
## 95%
#### Try C = 0.01
## 96%






## On another path, we Should Parse the output file from the PDF parser which will extract the features
### I will use PDFid from Dividier Stevens (this man is just awesome)
### I implemented a simple log file parser to extract the features.
### I will try now to only use those features and drop the other features because right now, I don't have a plan to extract them manually