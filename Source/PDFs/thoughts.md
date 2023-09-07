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
* header (contains erroneous values)
* encrypt (0 or 1 or -1) erroneous values are mapped to -1
* OpenAction (0 or 1 or -1, contains -1 and is cleansed of invalid entries)
* RichMedia
* launch (0 or 1 or -1)
* XFA (0 or 1 or -1)            --> XML Form Architecture, they are just forms same as login forms


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