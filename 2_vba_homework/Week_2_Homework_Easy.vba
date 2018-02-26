Sub StockAnalysis():
    Dim Current As Worksheet
    For Each Current In Worksheets
    
        Dim Ticker As String
        Dim Volume As Double
        Volume = 0
    
        Dim Summary_Table_Row As Integer
        Summary_Table_Row = 2
        Current.Range("I1").Value = "Ticker"
        Current.Range("J1").Value = "Volume"
    
        RowCount = Current.Cells(Rows.Count, "A").End(xlUp).Row
        
      For i = 2 To RowCount
        If Current.Cells(i + 1, 1).Value <> Current.Cells(i, 1).Value Then
            Ticker = Current.Cells(i, 1).Value
            Volume = Volume + Current.Cells(i, 7).Value
            Current.Range("I" & Summary_Table_Row).Value = Ticker
            Current.Range("J" & Summary_Table_Row).Value = Volume
            Summary_Table_Row = Summary_Table_Row + 1
            Volume = 0
    
        Else
          Volume = Volume + Current.Cells(i, 7).Value
    
        End If
    
        Next i

    Next

End Sub