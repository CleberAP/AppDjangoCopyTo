# AppDjangoCopyTo
App (Python + Tkinter) to copy your Django project to another directory.

---
<table>
  <tr>
    <td><img src="Telas/tela_01.png" width=250 title="image 1"/></td>
    <td><img src="Telas/tela_02.png" width=250 title="image 2"/></td>
  </tr>
</table>

---

This project was developed with two main purposes:
- App to copy an existing Django project to a Git directory on the computer;
- Demonstrate the application of Tkinter in the development of desktop solutions

**<p>This project is still under development, but what has been developed so far may arouse the curiosity of some students.</p>**
<p>The config.txt file contains the initial parameters, but the main one is the list of items blocked during copying, as it lists those that I consider not to be useful to upload to the repository. This way I didn't need to implement the gitignore.</p>
<p>Files or folders that you do not want to copy can be added to the list using the “Items NOT to copy” button. Clicking on it will open a window (image 2) for this purpose.</p>
<p>Such a window is implemented in the table_simple.py file. This file contains 3 classes: one creates a list (table) of elements; another creates a navigation bar; and the other a field for entering data into the list.</p>
<br>
<p>To define the source and destination directories, hover the cursor over the “Get Django Project Directory” and “Get Django Project Destination Directory” buttons.</p>
<p>To determine the destination folder (project name), it must exist in the chosen destination.</p>
<p>To create the folder (project name) check the 'Create Folder' checkbox and see that the project name, contained in the source path, will be inserted in the destination path.</p>
<hr>
<p>The .ico files were obtained from the [REMIX ICON website](https://remixicon.com/).</p>
