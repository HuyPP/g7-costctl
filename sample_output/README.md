# sample_output/

These files are **illustrative examples** showing the shape of `costctl`
output. They are NOT real account data.

When you submit, replace each `*_example.txt` with a real output from running
`costctl` against your workshop account. Then delete the example files.

## How to produce real samples

```bash
./costctl.py list ec2 > sample_output/list_ec2_$(date +%F).txt
./costctl.py list ec2 --missing-tag Application > sample_output/list_ec2_missing_app_$(date +%F).txt
./costctl.py cost --tag Application=<your-app> --days 7 > sample_output/cost_<your-app>_$(date +%F).txt
```

The trainer will `git clone` your repo, follow the README, and expect to
reproduce roughly these outputs (allowing for natural drift in timestamps and
resource lists between snapshots).

## Anti-pattern

Don't paste fabricated output. If `costctl list ec2` against your account
returns 0 rows, commit that — it's a valid output. Don't invent fake instance
IDs to make the sample look "interesting".


python costctl.py list ec2 > sample_output/list_ec2_2026-05-22.txt

EC2 all ù 2 found:
------------------------------------------------------------------------------
  i-0587a990ea27794b7       t3.micro       running      Name=testminilab
  i-0d21c60b074248839       t3.micro       running      Name=helloworld

python costctl.py list ec2 --missing-tag Application > sample_output/list_ec2_missing_app_2026-05-22.txt

EC2 missing:Application ù 2 found:
------------------------------------------------------------------------------
  i-0587a990ea27794b7       t3.micro       running      Name=testminilab
  i-0d21c60b074248839       t3.micro       running      Name=helloworld

python costctl.py list s3 > sample_output/list_s3_2026-05-22.txt

S3 all ù 5 found:
------------------------------------------------------------------------------
  minilab1111111            bucket         active       -
  myproduct-kb-191823465016 bucket         active       Application=SanGo,CostCenter=G7,Environment=dev,Owner=btn199919@gmail.com,aws:cloudformation:logical-id=S3Bucket,aws:cloudformation:stack-id=arn:aws:cloudformation:us-west-2:191823465016:stack/rag-w-bedrock-kb/9391f340-5379-11f1-a701-06090de1a25b,aws:cloudformation:stack-name=rag-w-bedrock-kb
  sango-static-assets-191823465016 bucket         active       Application=SanGo,CostCenter =G7,Environment=dev,Owner=btn199919@gmail.com
  sango-uploads-191823465016 bucket         active       Application=SanGo,CostCenter=G7,Environment=dev,Owner=btn199919@gmail.com
  w6-security-test-g7-191823465016-us-west-2-an bucket         active       -

python costctl.py terminate s3 --id minilab1111111 > sample_output/terminate_abort_2026-05-22.txt

Delete S3 bucket minilab1111111? [y/N] Deleted S3 minilab1111111

python costctl.py tag s3 --id myproduct-kb-191823465016 --set Application=SanGo --set CostCenter=G7 --set Environment=dev --set Owner=btn199919@gmail.com > sample_output/tag_s3_2026-05-22.txt

Applied 4 tag(s) to s3 myproduct-kb-191823465016: Application=SanGo, CostCenter=G7, Environment=dev, Owner=btn199919@gmail.com

PS E:\AWS\minilab\g7-costctl> python costctl.py cost --tag Application=SanGo --days 7 > sample_output/cost_sango_2026-05-22.txt

Cost for Application=SanGo over last 7 day(s): 1.8021342449 USD

