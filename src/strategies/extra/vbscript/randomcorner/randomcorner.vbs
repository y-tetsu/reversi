Option Explicit

Dim color
Dim board_size

' 標準入力の受け取り
color = WScript.StdIn.Readline()
board_size = WScript.StdIn.Readline()

Wscript.StdErr.WriteLine(color) 
Wscript.StdErr.WriteLine(board_size) 

Wscript.StdOut.WriteLine("0 0") 
