Option Explicit

Dim intColor
Dim intBoardSize
Dim intBoard()

'--------------------
' 標準入力の受け取り
'--------------------
intColor = WScript.StdIn.Readline() ' 手番
Wscript.StdErr.WriteLine(intColor)

intBoardSize = WScript.StdIn.Readline() ' 盤面サイズ
Wscript.StdErr.WriteLine(intBoardSize)

ReDim intBoard(intBoardSize-1, intBoardSize-1) ' 石の配置
Dim x
Dim y
For y=0 To intBoardSize-1
    Dim strLine
    Dim aryStrings
    Dim intTmp
    strLine = WScript.StdIn.ReadLine()
    Wscript.StdErr.WriteLine(strLine)
    aryStrings = Split(strLine, " ")
    For x=0 To intBoardSize-1
        intBoard(y, x) = aryStrings(x)
    Next
Next

'--------------------
' 手の候補を調べる
'--------------------



'--------------------
' 結果出力
'--------------------
'角がある場合は優先する
'それ以外はランダム
Wscript.StdOut.WriteLine("0 0")
