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
* 
