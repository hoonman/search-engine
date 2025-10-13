To-add to scraper logic
* when checking for valid links, we must ensure that the link tht we scraped is unique. must be done in the extract next link or is_valid function
*  urls that do not have to be downloaded are not added to the
frontier.
* permissions with robots.txt
* filter out non-links like mail-to, phone numbers. the link must be a valid link. (we are already doing this)
* multi-threaded crawler
* check similarity function (we should not check similar function based on a threshold)


* add proper content parsing due to corrupted bytes (check i think since we added resp_content = b"" for empty content or unparsable content)
* We must add respecting the delay code because i'm getting status 429 after a little while from plrg.ics.uci.edu we must add a specific delay --> not sure if we need this anymore 
* time the start and end (how long did the crawler take? ), how many urls ? -> we must add this.
* IMPORTANT: we need to figure out why valid_urls had duplicates in them. double-check unique urls logic.

* currently, since we fragment down the url into parsed.path.lower() and then extract invalid extensions, we are still processing certain urls with invalid paths. 
* first verify that this is a valid problem we should solve. and then 


* we must solve crashing issue but i feel like similarity detection will solve it automatically. so lets do this first and see if the crashing will be gone. 
* defragment links resolved the crashing issues.
* calendar traps 




## crawler report
* add the actual time the report finished (time.now into the json file)
