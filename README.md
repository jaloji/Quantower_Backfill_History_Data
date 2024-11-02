# Quantower_Backfill_History_Data

Description
-----
Because of some data provider don't save more than 1 month of tick data or anything like this you may want this script to import all the current contrat data.
This can be useful in case of you want a full volume profile.
Don't try to import a continous data if you don't have this feature with live account it will not be showed back in time more than your current contract.

Installation
-----
You need to edit the script and change:

```
database_name = "C:\\Users\\Path\\To\\Quantower\\AMP Quantower\\History\\AMP47CQG\\history.db"
```
You MUST have time set in UTC timezone (if you need to handle with timezone convertion use `pip install pytz`) and in dotnet tick format i've provided a exemple function to do this.

You may need to change this too as your data file have:
```
    values = line.split(";")
    price = float(values[0])
    # In case you need to covnert to dotnet tick time use and adapt this as you need
    # dt = datetime.strptime(date_part + time_part, "%Y%m%d%H%M%S")
    # time = convert_to_dotnet_ticks(dt)
    time = int(values[2])
    volume = float(values[3])
    aggressor = int(values[4])
    tick_direction = int(values[5])
    open_interest = float(values[6])
    buyer = values[7] if values[7] != 'None' else None
    seller = values[8] if values[8] != 'None' else None
    funding_rates = float(values[9]) if values[9] != 'None' else 0.0
    quote_asset_volume = values[10] if values[10] != 'None' else None
```

Usage
-----
To run this:

```
python.exe insert.py
```

WARNING !
-----
Once its imported you need to click on 'Refresh' only ! If you want to try 'Reload from server' do a backup of your history.db file.
Even with refresh it will downloads missing days or data if you have some but then it will use the data in your history.db fil when your provider don't have them.
So to have a history.db up-to-date you just need to do 'refresh' some time.
