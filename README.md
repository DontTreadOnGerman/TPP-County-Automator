# TPP-County-Automator
Automates the creation of county presets/county advanced options in The Political Process. Simply paste your county data into the attached CSV and run the script. You can even use your pre-existing advanced options if you've already got some great ones set up!

### Limitations
There aren't very many limitations, but there are some;
- It's recommended to round your county data to the nearest thousandth place, since exact division in any coding language is impossible (if you're confused, go to this [StackOverflow page.](https://stackoverflow.com/questions/588004/is-floating-point-math-broken))
- Windows is necessary for this script, as that's what TPP uses and other operating systems probably won't work.
- The county script replaces state leans in your advanced options, since that's how the game operates.
- You can only use this script to update every county at once - but if you want to change only a few counties, you should use extract_preset_counties.py, which'll save every county into a usable file. 

### Notes
- The preset used in the 2022 with flavor under examples was created by OregonMapGuy at [github.com/OregonMapGuy/2004Partisanship.](https://github.com/OregonMapGuy/2004Partisanship) All credit for that preset belongs to him - I simply overlayed it with 2022 county data.
- [All work is licensed under the MIT license.](https://github.com/DontTreadOnGerman/TPP-County-Automator/blob/main/LICENSE)
- You can view my other work, including my electoral models and maps, at [my website, acctuallydavid.com.](https://acctuallydavid.com) My twitter can be found at @davidsacc12345, and I'd appreciate if you followed my account.
