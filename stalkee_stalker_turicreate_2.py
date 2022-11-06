chin_ps = ( checkins.join( checkins, on = 'location_id' )
                    .rename( {'checkin_ts'   : 'checkin_ts_ee',
                              'checkin_ts.1' : 'checkin_ts_er',
                              'user_id'      : 'stalkee' ,
                              'user_id.1'    : 'stalker' } ) )

pairs_filtered = chin_ps[ (chin_ps['checkin_ts_ee'] < chin_ps['checkin_ts_er']) &
                          (chin_ps['stalkee'] != chin_ps['stalker]) ]

