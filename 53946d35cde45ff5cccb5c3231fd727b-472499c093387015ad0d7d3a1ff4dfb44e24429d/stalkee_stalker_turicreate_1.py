import turicreate as tc

checkins = ( tc.SFrame.read_csv( 'Gowalla_totalCheckins.txt',                  
                                 delimiter='\t', header=False )
                .rename( {'X1': 'user_id', 'X2' : 'checkin_ts',
                          'X3': 'lat', 'X4' : 'lon',
                          'X5': 'location_id'} )
  [["user_id", "location_id", "checkin_ts"]] )
