final_result = ( pairs_filtered[['stalkee', 'stalker', 'location_id']]
                    .unique()
                    .groupby( ['stalkee','stalker'] ,
                               {"location_count" : agg.COUNT })
                    .topk( 'location_count', k=5 )
                    .materialize() )

print( final_result ) 