// Test program

#include <iostream>
#include <fstream>
#include <curl/curl.h>
//#include <zip.h>

#include <vector>
#include <string>
#include <sstream>
#include <iterator>
//#include <libzip/zip.h>

using namespace std;

//insert into currency_rates (date, currency_pair, currency_rate) values ("1999-01-05", 'EUR/USD', 1.179);

vector<string> split(string s, char delim);

vector<string> parseCurrencyData(string currencyData);

size_t write_data(void *ptr, size_t size, size_t nmemb, FILE *stream) {
    size_t written = fwrite(ptr, size, nmemb, stream);
    return written;
}

double calculateDailyReturn(double dailyPrice[])
{
  /*double dailyReturn[] = dailyPrice;

  for (int i = 1; i < 5; i++)
    {
      dailyReturn[i-1] = 100 * (dailyPrice[i] - dailyPrice[i-1])/dailyPrice[i-1];
      cout << dailyReturn[i-1] << endl;
    }*/
  return 1.0;
}

double calculateVolatility()
{
    return 12.321;
}

bool downloadFile()
{
    CURL *curl;
    FILE *fp;
    CURLcode res;
    const char *url = "https://www.ecb.europa.eu/stats/eurofxref/eurofxref.zip?d4acbc94de4b8c8a6550ef5d9be07261";
    char outfilename[FILENAME_MAX] = "./ref_currency.zip";
    curl = curl_easy_init();
    if (curl) {
      fp = fopen(outfilename,"wb");
      curl_easy_setopt(curl, CURLOPT_URL, url); // "https://www.ecb.europa.eu/stats/eurofxref/eurofxref.zip?d4acbc94de4b8c8a6550ef5d9be07261");
      curl_easy_setopt(curl, CURLOPT_WRITEFUNCTION, write_data);
      curl_easy_setopt(curl, CURLOPT_WRITEDATA, fp);
      res = curl_easy_perform(curl);
      /* always cleanup */
      curl_easy_cleanup(curl);
      fclose(fp);
    }
    return true;
  
}


int main()
{
  //char *url[] = 'https://www.ecb.europa.eu/stats/eurofxref/eurofxref.zip?d4acbc94de4b8c8a6550ef5d9be07261';

  bool downloadSuccesful = downloadFile();
  ifstream currencyFile("./eurofxref.csv", ios::in);

  if (currencyFile.is_open())
    {
      string mainCurrencies[] = {"EUR", "USD", "JPY", "SEK", "CHF", "GBP", "CAD", "HKD", "AUD"};
      string line;
      unsigned int iter = 0;
      vector<string> currencyPairs;

      while (! currencyFile.eof() )
	{
	  getline (currencyFile,line);
	  
	  vector<string> result = parseCurrencyData(line);

	  if (iter == 0)
	    {
	      currencyPairs = result;
	    }
	  else
	    {
	      cout << result[0] << ": ";
	      string t_currencyRates;
	      for (unsigned int i = 1; i < result.size(); i++)
		{
		  if (result[i] != "N/A")
		    {
		      t_currencyRates += "EUR/" + currencyPairs[i] + ": " + result[i] + " ";
		    }
		}
	      cout << t_currencyRates << endl;
	    }
	  iter++;
	}
      currencyFile.close();
    }
  else
    {
      cout << "Could not open file" << endl;
    }

  return 0;
}

vector<string> split(string s, char delim = ',')
{
  vector<string> result;

  stringstream ss(s);
  string item;
  
  while(getline(ss, item, delim)) {
    result.push_back(item);
  } 
  return result;
}

vector<string> parseCurrencyData(string currencyData)
{
  vector<string> currencyRates = split(currencyData);
  return currencyRates;
}
