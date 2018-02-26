Sub StockAnalysis():
    Dim Current As Worksheet
    For Each Current In Worksheets
    
        Dim Ticker As String
        Dim OpenPrice As Double
        Dim ClosePrice As Double
        Dim YearlyChange As Double
        Dim PercentChange As Double
        Dim Volume As Double
        Volume = 0
    
        Dim Summary_Table_Row As Integer
        Summary_Table_Row = 2
        Current.Range("I1").Value = "Ticker"
        Current.Range("J1").Value = "Yearly Change"
        Current.Range("K1").Value = "Percent Change"
        Current.Range("L1").Value = "Total Stock Volume"
    
        RowCount = Current.Cells(Rows.Count, "A").End(xlUp).Row
        
      For i = 2 To RowCount
        If Current.Cells(i - 1, 1).Value <> Current.Cells(i, 1).Value Then
            OpenPrice = Current.Cells(i, 3).Value
        End If
        
        If Current.Cells(i + 1, 1).Value <> Current.Cells(i, 1).Value Then
            Ticker = Current.Cells(i, 1).Value
            ClosePrice = Current.Cells(i, 3).Value
            YearlyChange = OpenPrice - ClosePrice
            
            If OpenPrice <> 0 Then
                PercentChange = (YearlyChange / OpenPrice)
            Else
                PercentChange = 0
            End If
            
            If YearlyChange >= 0 Then
                 Current.Range("J" & Summary_Table_Row).Interior.ColorIndex = 4
            Else
                 Current.Range("J" & Summary_Table_Row).Interior.ColorIndex = 3
            End If
            
                
            Volume = Volume + Current.Cells(i, 7).Value
            Current.Range("I" & Summary_Table_Row).Value = Ticker
            Current.Range("J" & Summary_Table_Row).Value = YearlyChange
            Current.Range("K" & Summary_Table_Row).Value = PercentChange
            Current.Range("L" & Summary_Table_Row).Value = Volume
            Summary_Table_Row = Summary_Table_Row + 1
            Volume = 0
    
        Else
          Volume = Volume + Current.Cells(i, 7).Value
    
        End If
    
        Next i

    Next

End Sub