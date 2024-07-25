# ctrans_zh_en
- note: for Chinese abstract see [https://blog.csdn.net/sbsbsb666666/article/details/140693161](https://blog.csdn.net/sbsbsb666666/article/details/140693161)

This is a useful script for translate the comment in c(or c++) code from Chinese to English in batch!

firstly, python3 and following package is needed:
```bash
pip install  translators 
```
it will convert all Chinese comment of .c, .cpp or .h file in the same directory of this script with a simple run:
```bash
python trans.py
```

- **hint** :
you may also open the file in different encoding method, switch it in script by changing variable `open_encoding` (gbk or utf-8 is mostly used). also, setting `dst_decoding` to `utf-8` is recommended.

### Supported Comment Types for Translation
**Reminder:** back up your files before translating! If there are issues with the network or other problems during translation, files may be lost. So, make sure to back up first!
The following types of comments are supported for translation (examples of correct formats): 
```c
/*********** First Type ****************
* 中文注释1
* 中文注释2
**/
int a = 1;   // 中文注释1 (Can be translated to English)
int b = 2;   /* 中文注释2 (Correctly translated) */
int c = 3;   /* 中文注释3  
            * 中文注释4  (This format is also supported)
            */

// 中文注释5 (Translated Correctly)
/* 中文注释6 (can be translated) */
int func(){
}
```
### Non-Translatable Cases 
First, it should be noted that there are certain format requirements for comments to be translated, the format as below are not supported to be tranlated correctly:

- **Single-line comments:** If a single line starts directly with `//` or `/*`, the entire line will be considered a comment. For example, the following format is not allowed, i.e., it is not recommended to place comments before code:
  ```c
  /* Chinese comment */  int a = 1;
  ```

- **Multi-line comments:** Each line must start with `*`, otherwise, it will not be translated:
  ```c
  /*
   *   Correct statement: This sentence will be translated
       Incorrect: This sentence will not be translated since no asterisk at the start of the line 
   ******************/
  ```

- **Avoid using semicolons in comments:**
All comments should avoid using `;`, or it will be considered as a program statement and will not be translated:
  ```c
  /*
  *         This is a multi-line comment;      --->  Due to the semicolon, this will not be translated
  */
  ```

- **Do not move the semicolon to the next line:** For example:
  ```c
  int a = 1   // comment: The correct way is int a = 1; + comment
  ;
  ```
  This may cause the  program code in previous line to be translated as well.
