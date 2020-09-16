<h1> SADA-Systems <h1/>
Take home challenge. Challenge 2

For this challenge, I used a cloud environment to run my code. I ran my code with AWS Lambda collecting data S3. Attached in this 
repository are YAMl documents used to create the infrastructures needed. I used AWS because I am most comfortable working their infrasture.


<h2>
Read each non-blank line of text from the file loomings.txt available at

https://gist.github.com/bobbae/259e195f11cea0183ea93d378946a737
Print the total number of non-blank lines.


Create a file with a unique name containing each  non-blank line of  text read from  the file.
For example you may end up with lots of files. File-1, File-2, File-3, etc.
File-1 will contain the first line read from the file. File-2 will contain the second line
read from the file, and so on.


Create a companion file for each file. Each companion file will be a hash digest of the content of the file.
For example, File-1 may have a companion file named File-1.hash which will contain hash digest of the File-1.


List the files sorted based on the size of the file, in order, from smallest to largest based on the size (total bytes) of the content within the file. Print the name and size of each file on each line of the output.


There will be one duplicate line in the loomings.txt file. Therefore, there will be two companion (hash) files that have the same hash digest content.  Print the name of the two files that have identical content.
Print  the original  text line which is duplicated in loomings.txt.


Remove the duplicate (second occurance) line from loomings.txt and create a new version of the file and call it loomings-clean.txt.  Perform diff loomings*txt and produce output.



 
