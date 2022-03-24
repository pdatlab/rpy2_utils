# -*- coding: utf-8 -*-
"""

"""
import rpy2
import pandas as pd


class DataFrame():
    
    def __init__(self,r_df):
        """
        import rpy2_utils as ru
        dfh = ru.robjects.DataFrame(r_df)
        """
        
        #TODO: Verify data type
        self.r = r_df
    
    def __contains__(self, name):
        return name in self.r.names
    
    def renameColumn(self,old_name,new_name):
        names = list(self.r.names)
        I = names.index(old_name)
        self.r.names[I] = new_name
    
    @property
    def names(self):
        return self.r.names
    
    def __getitem__(self,name):
        names = list(self.r.names)
        I = names.index(name)
        r_column = self.r[I]
        
        #Had isinstance, but factor is subclass of int
        #to generally avoid subclass comparisons, switched to type()
        if type(r_column) == rpy2.robjects.vectors.IntVector:    
            return IntVector(r_column)
        elif type(r_column) == rpy2.robjects.vectors.StrVector:    
            return StrVector(r_column)
        elif type(r_column) == rpy2.robjects.vectors.FloatVector:
            return FloatVector(r_column)
        elif type(r_column) == rpy2.robjects.vectors.FactorVector:
            return FactorVector(r_column)
        else:
            raise Exception('Unhandled case')
    
    def __setitem__(self, name, new_value):
        names = list(self.r.names)
        I = names.index(name)
        self.r[I] = new_value.r
        


class IntVector():
    def __init__(self,r):
        self.r = r
        
    def as_factor(self,levels=None,ordered=False,na=None):
        
        if na is not None:
            raise Exception('NA option not yet handled for int vector')
        
        if levels is None:
            r = rpy2.robjects.vectors.FactorVector(self.r,ordered=ordered)
        else:
            levels_r = rpy2.robjects.vectors.IntVector(levels)
            r = rpy2.robjects.vectors.FactorVector(self.r,levels=levels_r,ordered=ordered)
        
        return FactorVector(r)

class StrVector():
    
    def __init__(self,r):
        self.r = r
        
    def as_factor(self,levels=None,ordered=False,na=None):
        
        if levels is None:
            if na is not None:
                raise Exception('NA for no levels specified not yet handled')
            r = rpy2.robjects.vectors.FactorVector(self.r,ordered=ordered)
        else:
            if na is not None:
                levels.remove(na)
                
            levels_r = rpy2.robjects.vectors.StrVector(levels)
            r = rpy2.robjects.vectors.FactorVector(self.r,levels=levels_r,ordered=ordered)
        
        # if na is not None:
        #     #TODO: Not sure if there is a better way of doing this ...
        #     final_levels = list(r.levels)
        #     I = final_levels.index(na)
        #     #Note, level values are 1 based, not 0 based
        #     I = I + 1
        #     r_column = self.r[I]
            
        #     #r_train_data.rx[r_train_data.ro == -1] = robjects.NA_Integer
            
        #     import pdb
        #     pdb.set_trace()
        #     pass
        
        return FactorVector(r)

class FloatVector():
    def __init__(self,r):
        self.r = r
        
class FactorVector():
    def __init__(self,r):
        self.r = r
        
    @property
    def levels(self):
        return self.r.levels
        
    def as_factor(self,levels=None,ordered=False,na=None):
        #TODO: it is possible this changes the levels
        #Right now this occurs when we rerun code that has 
        #already been converted
        return self
        
        
class FloatMatrix():
    def __init__(self,r):
        self.r = r      
        
    def as_dataframe(self):
        #TODO: Clean this up, can we just extract column values
        #   rather than build by row? Yes, slice by column
        #   n_rows = 5
        #   col1 = self.r[0:4]
        #   col2 = self.r[5:9]
        #   etc
        #
        #- make it so rownames is either a column (default) or index
        
        
        
        
        data = self.r
        col_names = ['rownames'] + list(data.colnames)
        row_names = data.rownames
        num_cols = data.ncol
        num_rows = data.nrow
        col_range = range(num_cols)
        row_range = range(num_rows)
    
    
        rows = []
        for x in row_range:
            index = [x+p*num_rows for p in col_range]
            row_values = [data[p] for p in index]
            row_values = [row_names[x]] + row_values
            row = dict(zip(col_names,row_values))
            row = pd.DataFrame(row, index=[x])
            rows.append(row)
            
        output = pd.concat(rows)
            
        return output
        