def parse(file, sheet, index): 
    x = pd.read_excel(file, sheet_name=sheet,header=None).values[:, index]
    x = x[~np.isnan(x)] # clean off nan
    return x

def readtrace(file, ci=0):  
    # read data frome excel
    exp = pd.read_excel(file, sheet_name=0,header=None).values[0, ci]
    t   = parse(file, 1, ci)
    x1  = parse(file, 2, ci)
    x2  = parse(file, 3, ci)
    bg1 = parse(file, 4, ci)
    bg2 = parse(file, 5, ci)
    dnp  = pd.read_excel(file, sheet_name=6,header=None).values[0, ci]
    return exp,t,x1,x2,bg1,bg2,dnp