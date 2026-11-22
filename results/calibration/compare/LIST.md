# calibration: a sample of the shared list trained again with a setting of the trainer changed

Masked MAE in the dataset-normalised unit, seed 0, the benchst split.  'stored' is the label of the benchst root.

## metrla: architectures of the shared list

**list/noinstnorm: 30 architectures.**

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

**list_patience/noinstnorm: 5 architectures.**

- val_mae: stored median 0.1819, best 0.1788; new median 0.1742, best 0.1692; median change -4.80 % (range -5.40 to -3.78); Spearman 0.300, Kendall 0.200; spread of the list (max - min) stored 0.0041, new 0.0055
- test_mae: stored median 0.1990, best 0.1964; new median 0.1869, best 0.1815; median change -6.84 % (range -7.58 to -3.15); Spearman 0.200, Kendall 0.200; spread of the list (max - min) stored 0.0043, new 0.0112
- the 5 best of the stored validation label have the new validation ranks [1, 5, 2, 4, 3]
- against the run of list/noinstnorm (5 architectures): median change of val_mae +0.0000, of test_mae -0.0000 (range -0.0006 to +0.0000)

| arch_id | stored val | stored test | new val | new test | epochs run | list/noinstnorm val | list/noinstnorm test | epochs run |
|---|---|---|---|---|---|---|---|---|
| 59d2d9e09e | 0.1788 | 0.1964 | 0.1692 | 0.1815 | 20 | 0.1692 | 0.1815 | 14 |
| 3bc0a1f7c2 | 0.1815 | 0.1990 | 0.1746 | 0.1928 | 20 | 0.1746 | 0.1928 | 18 |
| 598e82b0f7 | 0.1819 | 0.1999 | 0.1725 | 0.1862 | 20 | 0.1734 | 0.1864 | 9 |
| eb28991486 | 0.1827 | 0.1989 | 0.1746 | 0.1887 | 20 | 0.1746 | 0.1887 | 15 |
| b1ec9041e6 | 0.1830 | 0.2007 | 0.1742 | 0.1869 | 20 | 0.1737 | 0.1875 | 14 |

**list_top/noinstnorm: 24 architectures.**

- val_mae: stored median 0.1809, best 0.1778; new median 0.1752, best 0.1693; median change -3.03 % (range -5.51 to -1.03); Spearman 0.793, Kendall 0.609; spread of the list (max - min) stored 0.0049, new 0.0103
- test_mae: stored median 0.1995, best 0.1953; new median 0.1875, best 0.1820; median change -6.21 % (range -7.73 to -3.10); Spearman 0.654, Kendall 0.464; spread of the list (max - min) stored 0.0067, new 0.0126
- the 5 best of the stored validation label have the new validation ranks [3, 6, 2, 11, 1]

| arch_id | stored val | stored test | new val | new test | epochs run |
|---|---|---|---|---|---|
| 261470bcc0 | 0.1778 | 0.1953 | 0.1702 | 0.1835 | 12 |
| 43d20fa260 | 0.1784 | 0.1976 | 0.1727 | 0.1831 | 17 |
| 4bed16b516 | 0.1790 | 0.1972 | 0.1693 | 0.1820 | 17 |
| 78a96c05c4 | 0.1792 | 0.1975 | 0.1744 | 0.1851 | 13 |
| 8ddc39853c | 0.1792 | 0.1975 | 0.1693 | 0.1832 | 17 |
| 9d32d81fa5 | 0.1792 | 0.1975 | 0.1760 | 0.1890 | 9 |
| 6e62f26148 | 0.1797 | 0.1971 | 0.1715 | 0.1824 | 11 |
| 68a8b816fb | 0.1797 | 0.1979 | 0.1739 | 0.1877 | 18 |
| 236ae80505 | 0.1799 | 0.1976 | 0.1711 | 0.1844 | 17 |
| 2b8e049834 | 0.1802 | 0.1989 | 0.1764 | 0.1847 | 10 |
| d1015ae729 | 0.1805 | 0.1995 | 0.1759 | 0.1897 | 15 |
| 9e0e4f4c31 | 0.1807 | 0.1982 | 0.1740 | 0.1867 | 20 |
| 3c49ec9fdb | 0.1812 | 0.1996 | 0.1764 | 0.1921 | 10 |
| 6b07ab547f | 0.1812 | 0.2008 | 0.1737 | 0.1876 | 20 |
| 9708bac6db | 0.1815 | 0.2002 | 0.1796 | 0.1902 | 9 |
| c8b85a1bb8 | 0.1815 | 0.2003 | 0.1766 | 0.1874 | 12 |
| f7f783ef22 | 0.1817 | 0.2008 | 0.1768 | 0.1945 | 18 |
| 5a8ee1ef47 | 0.1818 | 0.1996 | 0.1746 | 0.1856 | 9 |
| c84e311c72 | 0.1819 | 0.2008 | 0.1741 | 0.1886 | 20 |
| 7871ccf3c4 | 0.1821 | 0.1998 | 0.1769 | 0.1903 | 9 |
| 9c5f19f758 | 0.1821 | 0.2020 | 0.1775 | 0.1891 | 10 |
| 44c802131d | 0.1826 | 0.2001 | 0.1784 | 0.1895 | 12 |
| dd70194123 | 0.1828 | 0.2011 | 0.1797 | 0.1899 | 12 |
| 6e608a90cf | 0.1828 | 0.2008 | 0.1769 | 0.1863 | 13 |

**Every run: 59 runs of 54 architectures.** Best test_mae 0.1815 (59d2d9e09e, list/noinstnorm); the run with the best val_mae (0.1692; 59d2d9e09e, list/noinstnorm) has test_mae 0.1815.

