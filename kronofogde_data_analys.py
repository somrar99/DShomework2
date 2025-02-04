import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def kronofogde_data_analys():
    # Read the CSV file with correct separator and encoding
    url = "https://kronofogden.entryscape.net/store/2/resource/238"
    try:
        df = pd.read_csv(url, encoding='iso-8859-1', sep=';')
        print("File read successfully.")
    except UnicodeDecodeError as e:
        print(f"Failed to read the file: {e}")
        return

    # Display the first few rows
    print(df.head(10))
    # Check if columns are parsed correctly
    print(df.info())

    # change the data type from 'object' to 'string'
    df['Län'] = df['Län'].astype('string')
    df['Kommun'] = df['Kommun'].astype('string')
    df['Persontyp'] = df['Persontyp'].astype('string')
    df['Kön'] = df['Kön'].astype('string')

    # Confirm that the changes take effect
    print(df.info())

    # calculate the unique kommun number
    lan_unique = df['Län'].unique()
    print(f'\nunique Län num = {lan_unique.size}')
    print(lan_unique)

    kommun_num = df['Kommun'].unique()
    print(f'\nunique kommun num = {kommun_num.size}')

    persontyp_num = df['Persontyp'].unique()
    print(f'\nunique persontyp num = {persontyp_num.size}')
    print(persontyp_num)

    gender_type = df['Kön'].unique()
    print(f'\n gender type num = {gender_type.size}')
    print(gender_type)

    year_range = df['År'].unique()
    print(f'\n year range : {year_range}')
    print(df['Kön'].unique())


    # drop na data
    df_dropna = df.dropna(how='all')
    # print('\n after dropna:')
    # df_dropna.info()

    # or fill the na data using 0
    df_filled = df.fillna(0)
    # print('\n after fillna:')
    # df_filled.info()

    # drop duplicated rows
    df_cleaned = df_filled.drop_duplicates()
    print('\n after drop_duplicates:')
    df_cleaned.info()

    df_cleaned["Belopp per person"] = df_cleaned["Belopp i kronor"] / df_cleaned["Antal beslut"]
    print('\n add new column:')
    df_cleaned.info()

    # save to excel file
    df_cleaned.to_excel("oskatt_ar 2018-2024.xlsx")

    # aggregate by Län
    df_lan = df_cleaned.groupby(['Län'])[['Antal beslut']].agg(['sum', 'mean', 'median'])
    df_lan.columns = ['Län_sum', 'Län_mean', 'Län_median']
    # print(df_lan)

    df_lan_sorted = df_lan.sort_values('Län', ascending=True)
    plt.figure(figsize=(12, 6))
    df_lan_sorted['Län_sum'].plot(kind='bar', color='#1f3a6d')
    plt.title('Totalt belopp per län från 2018 till 2024 (Kronor)')
    plt.xlabel('')
    plt.ylabel('Totalt belopp (SEK)')
    plt.xticks(rotation=45, ha='right')
    plt.savefig('totalt_belopp_per_län.png')
    plt.show()

    # line chart shows trend over time
    df_year = df_cleaned.groupby(['År'])[['Antal beslut']].agg(['sum', 'mean'])
    df_year.columns = ['year_sum', 'year_mean']
    print(df_year)

    plt.figure(figsize=(12, 6))
    df_year['year_sum'].plot(kind='line', marker='o', linestyle='-', color='#1f3a6d')
    plt.title('Totalt belopp från 2018 till 2024 (Kronor)')
    plt.xlabel('')
    plt.ylabel('Totalt belopp (SEK)')

    plt.savefig('totalt_belopp_2018_till_2024.png')
    plt.show()

    # hist Chart - focus on Stockholm
    df_sth = df_cleaned.query("Län =='STOCKHOLM'")
    # print("***")
    # print(df_sth)
    df_sth_male_2024 = df_sth.query("Kön == 'Man' and År == 2024")
    df_sth_female_2024 = df_sth.query("Kön == 'Kvinna' and År == 2024")
    # print(df_sth_male_2024)
    # print(df_sth_female_2024)
    fig, ax = plt.subplots(2, 1, figsize=(12, 8))
    df_sth_male_2024['Antal beslut'].plot(kind='hist', bins=30, edgecolor='black', ax=ax[0], color='#1f3a6d')
    ax[0].set_xlim(0, 12000)
    ax[0].set_ylim(0, 12)
    ax[0].set_title('Fördelning av Antal beslut för Man (STH, 2024)')
    ax[0].set_xlabel('Antal beslut')
    ax[0].set_ylabel('Antal kommun')

    df_sth_female_2024['Antal beslut'].plot(kind='hist', bins=30, edgecolor='black', ax=ax[1], color='#1f3a6d')
    ax[1].set_xlim(0,12000)
    ax[1].set_ylim(0, 12)
    ax[1].set_title('Fördelning av Antal beslut för Kvinna (STH, 2024)')
    ax[1].set_xlabel('Antal beslut')
    ax[1].set_ylabel('Antal kommun')

    plt.savefig('antal_beslut_man_och_kvinna.png')
    fig.tight_layout()
    plt.show()

    # scatter chart shows comparision between male, female and legal person
    df_sth_2024 = df_sth.query("År == 2024")
    # Create a scatter plot
    plt.figure(figsize=(12, 6))
    sns.scatterplot(
        data=df_sth_2024,
        x='Kommun',
        y='Antal beslut',
        hue='Kön',  # Different colors for each gender
        palette='Set1',  # Use a predefined color palette
        s=100,  # Size of the points
        # style='Persontyp'  # Different markers for gender
    )

    # Add labels and a title
    plt.title('Antal beslut för män, kvinna och juridisk mottagare', fontsize=14)
    plt.xticks(rotation=45, ha='right')
    plt.xlabel('Kommun', fontsize=12)
    plt.ylabel('Antal beslut', fontsize=12)
    plt.legend(title='Kön', fontsize=10)
    plt.grid(True)
    plt.savefig('antal_beslut_efter_kön.png')
    plt.show()



    # slutsatser
    # 1. Stockholm, Skåne och Västra Götaland är de tre länen med de högsta totalbeloppen 2018 till 2024
    # 2. Sveriges totalt belopp ökar från drygt 180 tusen år 2018 till ungefär 250 tusen  år 2024,  en genomsnittlig årlig ökning på 60 tusen
    # 3. Det totala antalet belopp är generellt sett högre för män jämfört med kvinnor i nästan alla kommuner. Specialt i Stockholm stad har män 11920 beslut, medan kvinnor har 6519.



kronofogde_data_analys()