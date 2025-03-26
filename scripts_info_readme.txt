Sr no       Script name                                                                         Description
-----------------------------------------------------------------------------------------------------------------------------------------------------------------
1.          validate_course                                                                     This will validate the course(parent+child), if any field is missing or not.
2.          url_cache                                                                           This will cache all the website url's in CDN.
3.          update_course_original_price                                                        This will update the course price in anquira from csv. NOTE: CSV must update before run.
4.          report
5.          rename_s3_file                                                                      This will rename the file which store on AWS S3.
6.          reminder_of_batch                                                                   This will send the reminder of batch before batch start. NOTE : time is 45 min - 1 Hr Before.
7.          reassign_counselor                                                                  This will change the owner of enquiry in anquira if enq not attend in 1 Hr.
8.          installment_paid_on                                                                 This will add a default "paid_on" date in Installments Table.
9.          import
10.         import_date
11.         genrate_certificate                                                                 This will genrate the student certificate on basic of end_date.
12.         download_recording                                                                  This will download the recording from Blue Jeans (link) and upload to AWS S3 Bucket.
13.         create_chat_room                                                                    This will create the chatroom on basic of batch.
14.         country_code                                                                        This will import all the country_code.
15.         check_recording_url_count                                                           This will check if the recording inc on yesterday or not, if not send a alert mail.
16.         change_username                                                                     This will change the username in users table, Replace "@" to "."
17.         change_update_on                                                                    This will change the update_on in enquiry Table.
18.         batch_time                                                                          This will send the email if instructor not join after batch time pass.
19.         batch_recording_url                                                                 This will fetch all the available recording url from blue jeans.
20.         anquira_summary_report                                                              
21.         anquira_course_price
22.         get_skills                                                                          This will genrate CSV of all skill/tags in parent courses.
23.         delete_junk_enquiry                                                                 This will delete all enquiry which mark as junk and its enquiry courses also.