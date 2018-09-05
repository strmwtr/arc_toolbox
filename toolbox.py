import arcpy

def print_fields(fc):
  '''Prints out the name of each field in fc using a for loop'''
  fields = [x.name for x in arcpy.ListFields(fc)]
  for x in fields:
    print (x)

def del_fields_by_keep(fc, keep_fields):
  '''Deletes all fields from fc not in keep_fields'''
  fields =[x.name for x in arcpy.ListFields(fc) if x.name not in keep_fields]
  arcpy.DeleteField_management(fc, fields)

def del_fields_by_del(fc, del_fields):
  '''Deletes all fields from fc not in del_fields'''
  arcpy.DeleteField_management(fc, del_fields)

def add_field(fc, field, field_type):
  '''Add a single field to fc'''
  arcpy.AddField_management (fc, field, field_type)

def add_list_of_fields(fc, list_of_fields):
  '''Add a list of fields to fc. list_of_fields format 
  [[field1, field_type1],[field2, field_type2],...]'''
  for x in list_of_fields:
    arcpy.AddField_management(fc, x[0],x[1])

def make_gdb(dir_path):
  '''Creates gdb at given location, ex: 'C:\sample.gdb' '''
  gdb_name = dir_path.split('\\')[-1]
  fldr = '\\'.join(dir_path.split('\\')[:-1])
  arcpy.CreateFileGDB_management(fldr, gdb_name)

def copy_item(src, dst):
  '''Copies feature or shp from src to dst'''
  arcpy.Copy_management(src, dst)

def delete(item_to_delete):
  '''Deletes any arc item, gdb/shp/feat/ect'''
  arcpy.Delete_management(item_to_delete)  

def calc_field1_to_field2(fc, src_field, dst_field):
  '''Does a field calculator to set src_field to dst_field'''
  with arcpy.da.UpdateCursor(fc, [src_field, dst_field]) as cursor:
    for row in cursor:
      row[1] = row[0]
      cursor.updateRow(row)

def intersect(list_of_feats, out_data):
  '''Runs intersect tool on list_of_feats and stores at out_data'''
  arcpy.Intersect_analysis(list_of_feats, out_data)

def address_field(in_table):
  '''Sets up an address field based on the MAT'''
  fields = ['ST_NUMBER', 'PREDIR', 'ST_NAME', 'SUFFIX', 'POSTDIR', 
    'UNIT_TYPE', 'ST_UNIT', 'Master_Address']
  with arcpy.da.UpdateCursor(in_table, fields) as cursor:
    for r in cursor:
        address = '{0} {1} {2} {3} {4} {5} {6}'.format(r[0],r[1],r[2],
          r[3],r[4],r[5],r[6])
        address = address.strip()
        while '  ' in address: address = address.replace('  ', ' ')
        r[-1] = address
        cursor.updateRow(r)

def edit_sde(func):
  '''Opens an editing session in sde and runs func. Do not put 
  parentheses after func. sample syntax - edit_sde(my_func)  '''
  db = r'Database Connections\Connection to GISPRDDB direct connect.sde'

  arcpy.env.workspace = db
  edit = arcpy.da.Editor(db)
  edit.startEditing(True,True)
  edit.startOperation()
  func()
  edit.stopOperation()
  edit.stopEditing(True)
  

#arcpy.ListFields (dataset, {wild_card}, {field_type})
#arcpy.DeleteField_management (in_table, drop_field)
#arcpy.CopyFeatures_management (in_features, out_feature_class, {config_keyword}, {spatial_grid_1}, {spatial_grid_2}, {spatial_grid_3})
#arcpy.Delete_management (in_data, {data_type})
#arcpy.MakeTableView_management (in_table, out_view, {where_clause}, {workspace}, {field_info})
#arcpy.Copy_management (in_data, out_data, {data_type})
#arcpy.SelectLayerByLocation_management (in_layer, {overlap_type}, {select_features}, {search_distance}, {selection_type}, {invert_spatial_relationship})
#arcpy.CreateFileGDB_management(dir, database_name.gdb)
#arcpy.MakeFeatureLayer_management(parcel, 'parcel_lyr')
