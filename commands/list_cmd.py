"""list — list AWS resources by type, filter by tag / missing-tag.

WHAT YOU MUST BUILD
-------------------
Support 4 resource types: ec2, rds, s3, volume.
Each takes:
- `want` — list of (key, value) tag pairs the resource MUST have
- `missing` — list of tag keys the resource MUST NOT have

Print a formatted table to stdout. Test cases are in tests/test_list.py.

HELPERS YOU CAN USE
-------------------
From commands._common:
  parse_kv(s) -> (k, v)            # "Owner=alice" -> ("Owner", "alice")
  tags_to_dict(items) -> dict       # boto3 [{"Key","Value"}] -> {k: v}
  tags_match(tags, want, missing) -> bool

AWS APIS YOU'LL NEED
--------------------
- EC2: ec2.describe_instances() with get_paginator
- RDS: rds.describe_db_instances(), then list_tags_for_resource(ResourceName=arn)
- S3:  s3.list_buckets(), then get_bucket_tagging(Bucket=name)
       (catch ClientError when bucket has no tagging config — treat as {})
- EBS: ec2.describe_volumes() with get_paginator

EXPECTED OUTPUT FORMAT (when run from CLI)
------------------------------------------
    EC2 Environment=dev — 1 found:
    ------------------------------------------------------------------------------
      i-0abc123def456789a       t3.micro       running       Environment=dev

VERIFY
------
    pytest tests/test_list.py -v
"""
import boto3
from botocore.exceptions import ClientError
from commands._common import parse_kv, tags_to_dict, tags_match


def _list_ec2(want, missing):
    ec2 = boto3.client("ec2", region_name="us-east-1")
    rows = []

    paginator = ec2.get_paginator("describe_instances")

    for page in paginator.paginate():
        for reservation in page.get("Reservations", []):
            for instance in reservation.get("Instances", []):
                tags = tags_to_dict(instance.get("Tags", []))

                if not tags_match(tags, want, missing):
                    continue

                rows.append(
                    (
                        instance["InstanceId"],
                        instance["InstanceType"],
                        instance["State"]["Name"],
                        tags,
                    )
                )

    return rows


def _list_rds(want, missing):
    rds = boto3.client("rds", region_name="us-east-1")
    rows = []

    paginator = rds.get_paginator("describe_db_instances")

    for page in paginator.paginate():
        for db in page.get("DBInstances", []):
            tag_resp = rds.list_tags_for_resource(
                ResourceName=db["DBInstanceArn"]
            )
            tags = tags_to_dict(tag_resp.get("TagList", []))

            if not tags_match(tags, want, missing):
                continue

            rows.append(
                (
                    db["DBInstanceIdentifier"],
                    db["DBInstanceClass"],
                    db["DBInstanceStatus"],
                    tags,
                )
            )

    return rows


def _list_s3(want, missing):
    s3 = boto3.client("s3", region_name="us-east-1")
    rows = []

    response = s3.list_buckets()

    for bucket in response.get("Buckets", []):
        name = bucket["Name"]

        try:
            tag_resp = s3.get_bucket_tagging(Bucket=name)
            tags = tags_to_dict(tag_resp.get("TagSet", []))
        except ClientError:
            tags = {}

        if not tags_match(tags, want, missing):
            continue

        rows.append((name, "bucket", "active", tags))

    return rows


def _list_volume(want, missing):
    ec2 = boto3.client("ec2", region_name="us-east-1")
    rows = []

    paginator = ec2.get_paginator("describe_volumes")

    for page in paginator.paginate():
        for volume in page.get("Volumes", []):
            tags = tags_to_dict(volume.get("Tags", []))

            if not tags_match(tags, want, missing):
                continue

            rows.append(
                (
                    volume["VolumeId"],
                    f'{volume["VolumeType"]}-{volume["Size"]}GB',
                    volume["State"],
                    tags,
                )
            )

    return rows

DISPATCH = {
    "ec2": _list_ec2,
    "rds": _list_rds,
    "s3": _list_s3,
    "volume": _list_volume,
}

def run(args):
    want = [parse_kv(tag) for tag in (args.tag or [])]
    missing = args.missing_tag or []

    rows = DISPATCH[args.type](want, missing)

    filters = []

    for key, value in want:
        filters.append(f"{key}={value}")

    for key in missing:
        filters.append(f"missing:{key}")

    filter_text = " ".join(filters) if filters else "all"

    print(f"{args.type.upper()} {filter_text} — {len(rows)} found:")
    print("-" * 78)

    for resource_id, resource_type, state, tags in rows:
        tag_text = "-"
        if tags:
            tag_text = ",".join(f"{k}={v}" for k, v in sorted(tags.items()))

        print(
            f"  {resource_id:<25} {resource_type:<14} {state:<12} {tag_text}"
        )