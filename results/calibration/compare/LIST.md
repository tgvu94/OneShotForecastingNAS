# calibration: a sample of the shared list trained again with a setting of the trainer changed

Masked MAE in the dataset-normalised unit, seed 0, the benchst split.  'stored' is the label of the benchst root.

## metrla: the sample of the shared list

**Variant noinstnorm: 30 of 30 architectures.**

- val_mae: stored median 0.1862, best 0.1788; new median 0.1796, best 0.1692; median change -3.64 % (range -6.11 to -0.08); Spearman 0.922, Kendall 0.761; spread of the list (max - min) stored 0.0234, new 0.0253
- test_mae: stored median 0.2056, best 0.1964; new median 0.1940, best 0.1815; median change -5.95 % (range -9.10 to -0.50); Spearman 0.852, Kendall 0.646; spread of the list (max - min) stored 0.0285, new 0.0341
- the 5 best of the stored validation label have the new validation ranks [1, 8, 7, 6, 3]

| arch_id | stored val | stored test | new val | new test | epochs run |
|---|---|---|---|---|---|
| 59d2d9e09e | 0.1788 | 0.1964 | 0.1692 | 0.1815 | 14 |
| 11e8af982e | 0.1796 | 0.1990 | 0.1755 | 0.1878 | 20 |
| f5b247bf7c | 0.1802 | 0.1994 | 0.1752 | 0.1901 | 20 |
| 3bc0a1f7c2 | 0.1815 | 0.1990 | 0.1746 | 0.1928 | 18 |
| 598e82b0f7 | 0.1819 | 0.1999 | 0.1734 | 0.1864 | 9 |
| eb28991486 | 0.1827 | 0.1989 | 0.1746 | 0.1887 | 15 |
| b1ec9041e6 | 0.1830 | 0.2007 | 0.1737 | 0.1875 | 14 |
| 298a922bd5 | 0.1833 | 0.2015 | 0.1755 | 0.1870 | 12 |
| c3afe62628 | 0.1835 | 0.2032 | 0.1795 | 0.1968 | 10 |
| f49573a790 | 0.1840 | 0.2014 | 0.1766 | 0.1876 | 15 |
| 6f77e842fa | 0.1844 | 0.2050 | 0.1731 | 0.1880 | 20 |
| f3ab66dc8c | 0.1847 | 0.2036 | 0.1768 | 0.1908 | 8 |
| 45cbf56658 | 0.1850 | 0.2020 | 0.1784 | 0.1924 | 18 |
| e82aa861b6 | 0.1855 | 0.2039 | 0.1768 | 0.1906 | 10 |
| 642b802236 | 0.1858 | 0.2079 | 0.1814 | 0.1951 | 20 |
| b03341cf63 | 0.1865 | 0.2069 | 0.1805 | 0.1963 | 12 |
| 3d2e516567 | 0.1872 | 0.2036 | 0.1797 | 0.1904 | 12 |
| 459821283b | 0.1877 | 0.2062 | 0.1774 | 0.1896 | 12 |
| f95c39cc83 | 0.1897 | 0.2103 | 0.1858 | 0.2058 | 14 |
| 7f1842236c | 0.1915 | 0.2124 | 0.1887 | 0.2001 | 15 |
| c06230db22 | 0.1925 | 0.2156 | 0.1853 | 0.1998 | 9 |
| 61d8caf5e4 | 0.1929 | 0.2144 | 0.1928 | 0.2060 | 14 |
| 7f4d7b46c9 | 0.1936 | 0.2147 | 0.1889 | 0.2006 | 10 |
| 8a14edd33a | 0.1943 | 0.2183 | 0.1898 | 0.2073 | 8 |
| cc1ea69864 | 0.1946 | 0.2168 | 0.1899 | 0.2157 | 13 |
| 2789069fda | 0.1952 | 0.2163 | 0.1938 | 0.2062 | 8 |
| 1b0f751e62 | 0.1958 | 0.2170 | 0.1916 | 0.2082 | 8 |
| ed7469df19 | 0.1967 | 0.2183 | 0.1918 | 0.2067 | 11 |
| a435209a10 | 0.1977 | 0.2207 | 0.1882 | 0.2008 | 8 |
| 1cda73d7c6 | 0.2023 | 0.2249 | 0.1945 | 0.2045 | 9 |

