Option Explicit
'============================================================
' RandomCorner : Get the corner. Otherwise random.
'============================================================

Dim intColor
Dim intSize
Dim intBoard()

Const BLANK = 0
Const BLACK = 1
Const WHITE = -1

'--------------------
' Get STDIN
'--------------------
intColor = CInt(WScript.StdIn.Readline()) ' Turn
Wscript.StdErr.WriteLine(intColor)

intSize = CInt(WScript.StdIn.Readline()) ' Board Size
Wscript.StdErr.WriteLine(intSize)

ReDim intBoard(intSize-1, intSize-1) ' Disc Position

Dim x
Dim y

For y=0 To intSize-1
    Dim strLine
    Dim aryStrings
    Dim intTmp

    strLine = WScript.StdIn.ReadLine()
    Wscript.StdErr.WriteLine(strLine)
    aryStrings = Split(strLine, " ")

    For x=0 To intSize-1
        intBoard(y, x) = CInt(aryStrings(x))
    Next

Next

'--------------------
' Get Leval Moves
'--------------------
Dim aryLegalMoves

aryLegalMoves = GetLegalMoves(intColor, intSize, intBoard)

'--------------------
' Output Result
'--------------------
Dim strNextMove

strNextMove = ""

Dim aryCorners
Dim strCorner
Dim strPossible
Dim intNum

aryCorners = Array("0 0", CStr(intSize-1) + " 0", "0 " + CStr(intSize-1), CStr(intSize-1) + " " + CStr(intSize-1))

For Each strCorner in aryCorners
    For Each strPossible in aryLegalMoves
        If strCorner = strPossible Then
            strNextMove = strCorner
            Wscript.StdErr.WriteLine("CORNER : "  + strCorner)
            Exit For
        End If
    Next

    If strNextMove <> "" Then
        Exit For
    End If
Next

If strNextMove = "" Then
    Randomize
    strNextMove = aryLegalMoves(Int(Rnd() * (Ubound(aryLegalMoves)+1)))
End If

Wscript.StdOut.WriteLine(strNextMove)


Function GetLegalMoves(intColor, intSize, intBoard)
    Dim aryLegalMoves()
    Dim intReversible
    Dim x
    Dim y
    Dim intCnt

    intCnt = 0

    For y=0 To intSize-1
        For x=0 To intSize-1
            intReversible = IsReversible(intColor, intSize, intBoard, x, y)

            If intReversible > 0 Then
                ReDim Preserve aryLegalMoves(intCnt)

                aryLegalMoves(intCnt) = CStr(x) + " " + CStr(y)
                Wscript.StdErr.WriteLine("POSSIBLE : " + CStr(x) + " " + CStr(y))
                intCnt = intCnt + 1
            End If
        Next
    Next

    GetLegalMoves = aryLegalMoves

End Function

Function IsReversible(intColor, intSize, intBoard, x, y)
    Dim intRet
    Dim aryDirs
    Dim aryDir

    intRet = 0
    aryDirs = Array(Array(-1, 1), Array(0, 1), Array(1, 1), Array(-1, 0), Array(1, 0), Array(-1, -1), Array(0, -1), Array(1, -1))

    If intBoard(y, x) = BLANK Then
        For Each aryDir in aryDirs
            Dim intNextX
            Dim intNextY
            Dim intTmp

            intNextX = x
            intNextY = y

            Do
                intNextX = intNextX + aryDir(0)
                intNextY = intNextY + aryDir(1)

                If (intNextX >= 0) And (intNextX < intSize) And (intNextY >= 0) And (intNextY < intSize) Then
                    Dim intNextValue

                    intNextValue = intBoard(intNextY, intNextX)

                    If intNextValue <> BLANK Then
                        If intNextValue = intColor Then
                            Exit Do
                        End If

                        intTmp = intTmp + 1
                    Else
                        intTmp = 0
                        Exit Do
                    End If
                Else
                    intTmp = 0
                    Exit Do
                End If
            Loop

            intRet = intRet + intTmp
        Next
    End If

    IsReversible = intRet

End Function
'============================================================
' END
'============================================================
