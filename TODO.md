[Steps:]
    [-][Authentication]:
        =
        [Login=#Token-Obtain]: Email - Password #-[Apple-Facebook-Google] 
        = If SignUP With Social Redirect To [Create-Account] pass Email
        =
        [Forget-Password]: With -Email => Code Sent to mail => [Verify-Code-4-Digits]
        =
        [Create-Account]: Email - Password - First Name - Last Name - Country - Phone Number - avatar-img - Avatar 'Set Default Img'
        =
        ===============================
    [-][Bussiness-Info]:
        [Default->Post-Put]Service Title - Country - Currency
        ===============================
    [-][Service]:
        *[Bussiness Information]* [Post-Put]Service Title - Country - Currency
        =
        [Services-Post-Put-Delete-ListRetieve] Service-Name - Service Description - Amount/Units
        - Amount: Int Field +#Currency
        - Units: Unit Name * UnitPrice
        ===============================
    [-][Income] overall income - collected - remaining -> highest income service
    =
    =
    [-][Expenses] overall expenses - paid - remainig -> highest paid expence 
    = [Expenses-Category]
    = [Payment] Date Selection - Expenses Category - Assistant Salaries - Remainig assistant salary - total expenses amount - total remaining - settle date
