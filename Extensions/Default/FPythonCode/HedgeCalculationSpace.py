
import acm

scsc = acm.Calculations().CreateStandardCalculationsSpaceCollection()


def create_timebuckets(bucket_lables):
    buckets_definition =[]
    for label in bucket_lables:
        bucket_definition = acm.FFixedDateTimeBucketDefinition()
        bucket_definition.FixedDate(label)
        buckets_definition.append(bucket_definition)
    definition = acm.TimeBuckets().CreateTimeBucketsDefinition(0,
            buckets_definition, False, False, False, False, False)
    def_and_conf = acm.TimeBuckets().CreateTimeBucketsDefinitionAndConfiguration(definition)
    return acm.TimeBuckets().CreateTimeBuckets(def_and_conf)
