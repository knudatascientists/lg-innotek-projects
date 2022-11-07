{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": 1,
   "id": "bc4ae654",
   "metadata": {},
   "outputs": [],
   "source": [
    "import numpy as np\n",
    "import pandas as pd"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 2,
   "id": "acf01274",
   "metadata": {},
   "outputs": [],
   "source": [
    "DIR1='./l.csv'\n",
    "DIR2='./m.csv'\n",
    "DIR3='./n.csv'\n",
    "DIR4='./o.csv'\n",
    "DIR5='./p.csv'\n",
    "DIR6='./q.csv'"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 3,
   "id": "5a866ab1",
   "metadata": {},
   "outputs": [
    {
     "name": "stderr",
     "output_type": "stream",
     "text": [
      "C:\\Users\\USER\\AppData\\Local\\Temp\\ipykernel_2756\\2332636513.py:6: DtypeWarning: Columns (1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,51,52,53,54,55,56,57,58,59,60,61,62,63,64,65,66,67,68,69,70) have mixed types. Specify dtype option on import or set low_memory=False.\n",
      "  df6=pd.read_csv(DIR6, header=None)\n"
     ]
    }
   ],
   "source": [
    "df1=pd.read_csv(DIR1, header=None)\n",
    "df2=pd.read_csv(DIR2, header=None)\n",
    "df3=pd.read_csv(DIR3, header=None)\n",
    "df4=pd.read_csv(DIR4, header=None)\n",
    "df5=pd.read_csv(DIR5, header=None)\n",
    "df6=pd.read_csv(DIR6, header=None)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 4,
   "id": "5dbcc78b",
   "metadata": {},
   "outputs": [],
   "source": [
    "df1.drop_duplicates(subset=0, keep='last', inplace=True)\n",
    "df2.drop_duplicates(subset=0, keep='last', inplace=True)\n",
    "df3.drop_duplicates(subset=0, keep='last', inplace=True)\n",
    "df4.drop_duplicates(subset=0, keep='last', inplace=True)\n",
    "df5.drop_duplicates(subset=0, keep='last', inplace=True)\n",
    "df6.drop_duplicates(subset=0, keep='last', inplace=True)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 5,
   "id": "1b1c94c1",
   "metadata": {},
   "outputs": [],
   "source": [
    "df1=df1.set_index(0)\n",
    "df2=df2.set_index(0)\n",
    "df3=df3.set_index(0)\n",
    "df4=df4.set_index(0)\n",
    "df5=df5.set_index(0)\n",
    "df6=df6.set_index(0)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 6,
   "id": "be48d56f",
   "metadata": {},
   "outputs": [],
   "source": [
    "# 1. Log 파일 합치기\n",
    "dfall=pd.concat([df1,df2,df3,df4,df5,df6], join='inner', axis=1) # ignore_index= 'bool'"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 7,
   "id": "af03099e",
   "metadata": {},
   "outputs": [],
   "source": [
    "# 2. Log들을 바코드 순(사전 순)으로 정렬\n",
    "dfall=dfall.sort_values([0], ascending=True)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 8,
   "id": "f70f63b7",
   "metadata": {},
   "outputs": [],
   "source": [
    "dfall.iloc[1:,:] = dfall.iloc[1:,:].astype('float')"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 9,
   "id": "787cefdc",
   "metadata": {},
   "outputs": [],
   "source": [
    "row = dfall.shape[0]\n",
    "col = dfall.shape[1]"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 10,
   "id": "e3ef0bbe",
   "metadata": {},
   "outputs": [],
   "source": [
    "dfall[' '] = np.nan\n",
    "dfall.iloc[2,290] = 'result'\n",
    "dfall.iloc[:2,290] = ' '"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 11,
   "id": "3ccdcc94",
   "metadata": {},
   "outputs": [],
   "source": [
    "for i in range(row-3):\n",
    "    res = []\n",
    "    for j in range(col-1):\n",
    "        a = dfall.iloc[i+3,j]\n",
    "        high = dfall.iloc[1,j]\n",
    "        low = dfall.iloc[2,j]\n",
    "    \n",
    "        if a > high or a < low:\n",
    "            res.append(dfall.iloc[0,j])\n",
    "        else:\n",
    "            pass\n",
    "    if res == []:\n",
    "        dfall.iloc[i+3, 290] = \"pass\"\n",
    "    else:\n",
    "        dfall.iloc[i+3, 290] = ' '.join(res)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 12,
   "id": "6efc7beb",
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/html": [
       "<div>\n",
       "<style scoped>\n",
       "    .dataframe tbody tr th:only-of-type {\n",
       "        vertical-align: middle;\n",
       "    }\n",
       "\n",
       "    .dataframe tbody tr th {\n",
       "        vertical-align: top;\n",
       "    }\n",
       "\n",
       "    .dataframe thead th {\n",
       "        text-align: right;\n",
       "    }\n",
       "</style>\n",
       "<table border=\"1\" class=\"dataframe\">\n",
       "  <thead>\n",
       "    <tr style=\"text-align: right;\">\n",
       "      <th></th>\n",
       "      <th>1</th>\n",
       "      <th>2</th>\n",
       "      <th>3</th>\n",
       "      <th>4</th>\n",
       "      <th>5</th>\n",
       "      <th>6</th>\n",
       "      <th>7</th>\n",
       "      <th>8</th>\n",
       "      <th>9</th>\n",
       "      <th>10</th>\n",
       "      <th>...</th>\n",
       "      <th>62</th>\n",
       "      <th>63</th>\n",
       "      <th>64</th>\n",
       "      <th>65</th>\n",
       "      <th>66</th>\n",
       "      <th>67</th>\n",
       "      <th>68</th>\n",
       "      <th>69</th>\n",
       "      <th>70</th>\n",
       "      <th></th>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>0</th>\n",
       "      <th></th>\n",
       "      <th></th>\n",
       "      <th></th>\n",
       "      <th></th>\n",
       "      <th></th>\n",
       "      <th></th>\n",
       "      <th></th>\n",
       "      <th></th>\n",
       "      <th></th>\n",
       "      <th></th>\n",
       "      <th></th>\n",
       "      <th></th>\n",
       "      <th></th>\n",
       "      <th></th>\n",
       "      <th></th>\n",
       "      <th></th>\n",
       "      <th></th>\n",
       "      <th></th>\n",
       "      <th></th>\n",
       "      <th></th>\n",
       "      <th></th>\n",
       "    </tr>\n",
       "  </thead>\n",
       "  <tbody>\n",
       "    <tr>\n",
       "      <th>barcode</th>\n",
       "      <td>LB</td>\n",
       "      <td>LC</td>\n",
       "      <td>LD</td>\n",
       "      <td>LE</td>\n",
       "      <td>LF</td>\n",
       "      <td>LG</td>\n",
       "      <td>LH</td>\n",
       "      <td>LI</td>\n",
       "      <td>LJ</td>\n",
       "      <td>LK</td>\n",
       "      <td>...</td>\n",
       "      <td>QBK</td>\n",
       "      <td>QBL</td>\n",
       "      <td>QBM</td>\n",
       "      <td>QBN</td>\n",
       "      <td>QBO</td>\n",
       "      <td>QBP</td>\n",
       "      <td>QBQ</td>\n",
       "      <td>QBR</td>\n",
       "      <td>QBS</td>\n",
       "      <td></td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>high limit</th>\n",
       "      <td>15.0</td>\n",
       "      <td>15.0</td>\n",
       "      <td>120.0</td>\n",
       "      <td>12.0</td>\n",
       "      <td>52.0</td>\n",
       "      <td>4550.0</td>\n",
       "      <td>2.0</td>\n",
       "      <td>-0.35</td>\n",
       "      <td>-0.35</td>\n",
       "      <td>-0.18</td>\n",
       "      <td>...</td>\n",
       "      <td>2.2</td>\n",
       "      <td>2.2</td>\n",
       "      <td>2.2</td>\n",
       "      <td>2.2</td>\n",
       "      <td>2.2</td>\n",
       "      <td>2.2</td>\n",
       "      <td>2.2</td>\n",
       "      <td>2.2</td>\n",
       "      <td>2.2</td>\n",
       "      <td></td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>low limit</th>\n",
       "      <td>2.0</td>\n",
       "      <td>2.0</td>\n",
       "      <td>20.0</td>\n",
       "      <td>0.5</td>\n",
       "      <td>0.5</td>\n",
       "      <td>0.5</td>\n",
       "      <td>0.0</td>\n",
       "      <td>-0.8</td>\n",
       "      <td>-0.8</td>\n",
       "      <td>-0.5</td>\n",
       "      <td>...</td>\n",
       "      <td>1.05</td>\n",
       "      <td>1.05</td>\n",
       "      <td>1.05</td>\n",
       "      <td>1.05</td>\n",
       "      <td>1.05</td>\n",
       "      <td>1.05</td>\n",
       "      <td>1.05</td>\n",
       "      <td>1.05</td>\n",
       "      <td>1.05</td>\n",
       "      <td>result</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>module100</th>\n",
       "      <td>9.082684</td>\n",
       "      <td>9.082684</td>\n",
       "      <td>55.177303</td>\n",
       "      <td>6.630663</td>\n",
       "      <td>17.534422</td>\n",
       "      <td>123.035645</td>\n",
       "      <td>0.038511</td>\n",
       "      <td>-0.409231</td>\n",
       "      <td>-0.414945</td>\n",
       "      <td>-0.229011</td>\n",
       "      <td>...</td>\n",
       "      <td>1.618154</td>\n",
       "      <td>1.617288</td>\n",
       "      <td>1.587904</td>\n",
       "      <td>1.580392</td>\n",
       "      <td>1.587695</td>\n",
       "      <td>1.596796</td>\n",
       "      <td>1.59231</td>\n",
       "      <td>1.581199</td>\n",
       "      <td>1.575421</td>\n",
       "      <td>pass</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>module1006</th>\n",
       "      <td>9.650352</td>\n",
       "      <td>9.990952</td>\n",
       "      <td>57.902111</td>\n",
       "      <td>5.893923</td>\n",
       "      <td>16.208288</td>\n",
       "      <td>143.959076</td>\n",
       "      <td>0.037601</td>\n",
       "      <td>-0.418462</td>\n",
       "      <td>-0.416703</td>\n",
       "      <td>-0.231209</td>\n",
       "      <td>...</td>\n",
       "      <td>1.594336</td>\n",
       "      <td>1.587632</td>\n",
       "      <td>1.572886</td>\n",
       "      <td>1.56796</td>\n",
       "      <td>1.574067</td>\n",
       "      <td>1.57847</td>\n",
       "      <td>1.580842</td>\n",
       "      <td>1.571393</td>\n",
       "      <td>1.563038</td>\n",
       "      <td>pass</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>...</th>\n",
       "      <td>...</td>\n",
       "      <td>...</td>\n",
       "      <td>...</td>\n",
       "      <td>...</td>\n",
       "      <td>...</td>\n",
       "      <td>...</td>\n",
       "      <td>...</td>\n",
       "      <td>...</td>\n",
       "      <td>...</td>\n",
       "      <td>...</td>\n",
       "      <td>...</td>\n",
       "      <td>...</td>\n",
       "      <td>...</td>\n",
       "      <td>...</td>\n",
       "      <td>...</td>\n",
       "      <td>...</td>\n",
       "      <td>...</td>\n",
       "      <td>...</td>\n",
       "      <td>...</td>\n",
       "      <td>...</td>\n",
       "      <td>...</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>module963</th>\n",
       "      <td>7.947349</td>\n",
       "      <td>8.742084</td>\n",
       "      <td>57.675041</td>\n",
       "      <td>6.335967</td>\n",
       "      <td>17.239725</td>\n",
       "      <td>130.255707</td>\n",
       "      <td>0.030788</td>\n",
       "      <td>-0.421978</td>\n",
       "      <td>-0.422857</td>\n",
       "      <td>-0.232967</td>\n",
       "      <td>...</td>\n",
       "      <td>1.624316</td>\n",
       "      <td>1.625815</td>\n",
       "      <td>1.594829</td>\n",
       "      <td>1.595796</td>\n",
       "      <td>1.613415</td>\n",
       "      <td>1.622312</td>\n",
       "      <td>1.62326</td>\n",
       "      <td>1.606579</td>\n",
       "      <td>1.589734</td>\n",
       "      <td>pass</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>module965</th>\n",
       "      <td>9.763885</td>\n",
       "      <td>9.196218</td>\n",
       "      <td>54.041969</td>\n",
       "      <td>5.599227</td>\n",
       "      <td>17.387074</td>\n",
       "      <td>169.155594</td>\n",
       "      <td>0.04574</td>\n",
       "      <td>-0.421978</td>\n",
       "      <td>-0.420659</td>\n",
       "      <td>-0.23033</td>\n",
       "      <td>...</td>\n",
       "      <td>1.675339</td>\n",
       "      <td>1.676941</td>\n",
       "      <td>1.662236</td>\n",
       "      <td>1.65427</td>\n",
       "      <td>1.667557</td>\n",
       "      <td>1.677775</td>\n",
       "      <td>1.676856</td>\n",
       "      <td>1.660233</td>\n",
       "      <td>1.650687</td>\n",
       "      <td>pass</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>module976</th>\n",
       "      <td>5.336077</td>\n",
       "      <td>0.0</td>\n",
       "      <td>31.562326</td>\n",
       "      <td>6.188619</td>\n",
       "      <td>17.387074</td>\n",
       "      <td>132.02388</td>\n",
       "      <td>0.042255</td>\n",
       "      <td>-0.422418</td>\n",
       "      <td>-0.421978</td>\n",
       "      <td>-0.23033</td>\n",
       "      <td>...</td>\n",
       "      <td>0.0</td>\n",
       "      <td>0.0</td>\n",
       "      <td>0.0</td>\n",
       "      <td>0.0</td>\n",
       "      <td>0.0</td>\n",
       "      <td>0.0</td>\n",
       "      <td>0.0</td>\n",
       "      <td>0.0</td>\n",
       "      <td>0.0</td>\n",
       "      <td>LC LM LAA LAB LAC LAD LAF LAG LAH LAI LAJ LAK ...</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>module989</th>\n",
       "      <td>9.423285</td>\n",
       "      <td>9.309751</td>\n",
       "      <td>58.469776</td>\n",
       "      <td>6.188619</td>\n",
       "      <td>16.355637</td>\n",
       "      <td>143.369675</td>\n",
       "      <td>0.043362</td>\n",
       "      <td>-0.426813</td>\n",
       "      <td>-0.425055</td>\n",
       "      <td>-0.232088</td>\n",
       "      <td>...</td>\n",
       "      <td>1.598823</td>\n",
       "      <td>1.602053</td>\n",
       "      <td>1.573707</td>\n",
       "      <td>1.574946</td>\n",
       "      <td>1.587901</td>\n",
       "      <td>1.59732</td>\n",
       "      <td>1.593059</td>\n",
       "      <td>1.580063</td>\n",
       "      <td>1.568402</td>\n",
       "      <td>pass</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>module992</th>\n",
       "      <td>8.060882</td>\n",
       "      <td>7.720281</td>\n",
       "      <td>57.107376</td>\n",
       "      <td>6.778011</td>\n",
       "      <td>17.239725</td>\n",
       "      <td>143.369675</td>\n",
       "      <td>0.034851</td>\n",
       "      <td>-0.423297</td>\n",
       "      <td>-0.424615</td>\n",
       "      <td>-0.235604</td>\n",
       "      <td>...</td>\n",
       "      <td>1.645905</td>\n",
       "      <td>1.648911</td>\n",
       "      <td>1.638902</td>\n",
       "      <td>1.640148</td>\n",
       "      <td>1.645316</td>\n",
       "      <td>1.643433</td>\n",
       "      <td>1.644732</td>\n",
       "      <td>1.642701</td>\n",
       "      <td>1.642499</td>\n",
       "      <td>pass</td>\n",
       "    </tr>\n",
       "  </tbody>\n",
       "</table>\n",
       "<p>331 rows × 291 columns</p>\n",
       "</div>"
      ],
      "text/plain": [
       "                   1         2          3         4          5           6  \\\n",
       "0                                                                            \n",
       "barcode           LB        LC         LD        LE         LF          LG   \n",
       "high limit      15.0      15.0      120.0      12.0       52.0      4550.0   \n",
       "low limit        2.0       2.0       20.0       0.5        0.5         0.5   \n",
       "module100   9.082684  9.082684  55.177303  6.630663  17.534422  123.035645   \n",
       "module1006  9.650352  9.990952  57.902111  5.893923  16.208288  143.959076   \n",
       "...              ...       ...        ...       ...        ...         ...   \n",
       "module963   7.947349  8.742084  57.675041  6.335967  17.239725  130.255707   \n",
       "module965   9.763885  9.196218  54.041969  5.599227  17.387074  169.155594   \n",
       "module976   5.336077       0.0  31.562326  6.188619  17.387074   132.02388   \n",
       "module989   9.423285  9.309751  58.469776  6.188619  16.355637  143.369675   \n",
       "module992   8.060882  7.720281  57.107376  6.778011  17.239725  143.369675   \n",
       "\n",
       "                   7         8         9        10  ...        62        63  \\\n",
       "0                                                   ...                       \n",
       "barcode           LH        LI        LJ        LK  ...       QBK       QBL   \n",
       "high limit       2.0     -0.35     -0.35     -0.18  ...       2.2       2.2   \n",
       "low limit        0.0      -0.8      -0.8      -0.5  ...      1.05      1.05   \n",
       "module100   0.038511 -0.409231 -0.414945 -0.229011  ...  1.618154  1.617288   \n",
       "module1006  0.037601 -0.418462 -0.416703 -0.231209  ...  1.594336  1.587632   \n",
       "...              ...       ...       ...       ...  ...       ...       ...   \n",
       "module963   0.030788 -0.421978 -0.422857 -0.232967  ...  1.624316  1.625815   \n",
       "module965    0.04574 -0.421978 -0.420659  -0.23033  ...  1.675339  1.676941   \n",
       "module976   0.042255 -0.422418 -0.421978  -0.23033  ...       0.0       0.0   \n",
       "module989   0.043362 -0.426813 -0.425055 -0.232088  ...  1.598823  1.602053   \n",
       "module992   0.034851 -0.423297 -0.424615 -0.235604  ...  1.645905  1.648911   \n",
       "\n",
       "                  64        65        66        67        68        69  \\\n",
       "0                                                                        \n",
       "barcode          QBM       QBN       QBO       QBP       QBQ       QBR   \n",
       "high limit       2.2       2.2       2.2       2.2       2.2       2.2   \n",
       "low limit       1.05      1.05      1.05      1.05      1.05      1.05   \n",
       "module100   1.587904  1.580392  1.587695  1.596796   1.59231  1.581199   \n",
       "module1006  1.572886   1.56796  1.574067   1.57847  1.580842  1.571393   \n",
       "...              ...       ...       ...       ...       ...       ...   \n",
       "module963   1.594829  1.595796  1.613415  1.622312   1.62326  1.606579   \n",
       "module965   1.662236   1.65427  1.667557  1.677775  1.676856  1.660233   \n",
       "module976        0.0       0.0       0.0       0.0       0.0       0.0   \n",
       "module989   1.573707  1.574946  1.587901   1.59732  1.593059  1.580063   \n",
       "module992   1.638902  1.640148  1.645316  1.643433  1.644732  1.642701   \n",
       "\n",
       "                  70                                                     \n",
       "0                                                                        \n",
       "barcode          QBS                                                     \n",
       "high limit       2.2                                                     \n",
       "low limit       1.05                                             result  \n",
       "module100   1.575421                                               pass  \n",
       "module1006  1.563038                                               pass  \n",
       "...              ...                                                ...  \n",
       "module963   1.589734                                               pass  \n",
       "module965   1.650687                                               pass  \n",
       "module976        0.0  LC LM LAA LAB LAC LAD LAF LAG LAH LAI LAJ LAK ...  \n",
       "module989   1.568402                                               pass  \n",
       "module992   1.642499                                               pass  \n",
       "\n",
       "[331 rows x 291 columns]"
      ]
     },
     "execution_count": 12,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "dfall"
   ]
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3 (ipykernel)",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.9.12"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 5
}