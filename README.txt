EAGLE'S NEST RESORT — SIMPLE SITE (site simple 1.4)
==================================================================
A cut-down version, ready to put live today.


WHAT TO UPLOAD
------------------------------------------------------------------
Upload everything in this folder to the root of your web host,
keeping the structure as it is:

    index.html            The home page — the real thing
    lodge.html            A gallery of the property
    getting-here.html     "Coming soon"
    things-to-do.html     "Coming soon"
    hosts.html            "Coming soon"

    css/site.css
    js/site.js
    images/               11 files
    images/gal/           34 gallery thumbnails
    images/lg/            34 larger versions for the viewer
    _headers              cache rules (Netlify; harmless elsewhere)

11 MB in total. Delete this README before going live if you like.


HOW IT BEHAVES
------------------------------------------------------------------
- The HOME PAGE is complete. Hero, the Highway 20 map, the lodge
  carousel, the hosts introduction, the two guest reviews, and the
  closing call to action.

- THE LODGE is a gallery: 34 photographs of the property in a
  grid, any of which opens larger. Arrow keys and swipe move
  between them, Escape or a downward swipe closes. Under it, a
  short note that rooms and rates are still to come, with the
  phone number and email address.

- The three other nav items each open a real page saying that
  section is on its way, with your phone number, email address and
  address on it. Nobody hits a dead link or a 404.

- BOOKING goes straight to your Booking.com listing, in a new tab.
  Every Booking link does this: the header button, the buttons on
  the home page, and the footer link.


ADDING OR REMOVING GALLERY PHOTOS
------------------------------------------------------------------
Each photo needs two files:

  images/gal/<name>.jpg   680px wide, shown in the grid
  images/lg/<name>.jpg    1100px wide, opens when tapped

Then copy one of the button blocks in lodge.html:

    <button class="gitem" type="button">
      <img src="images/gal/YOUR-PHOTO.jpg"
           data-full="images/lg/YOUR-PHOTO.jpg"
           loading="lazy" decoding="async"
           alt="Describe what is in the photo.">
      <span class="cap">Caption</span>
    </button>

To remove one, delete its block. Update the count in the line
below the grid if you want it exact.


CHANGING THE BOOKING LINK
------------------------------------------------------------------
The Booking.com URL appears several times. To change it, search
every .html file for:

    booking.com/hotel/ca/anahim-lake

and replace the whole href. They all open in a new tab via
target="_blank" rel="noopener noreferrer" — keep those attributes.


TURNING THE FULL PAGES ON LATER
------------------------------------------------------------------
The complete versions of The Lodge, Getting Here, Things To Do and
Your Hosts already exist in the full build. When you're ready,
replace the "coming soon" files with the real ones and upload the
extra images they need.

Do not mix the two builds halfway. The full Lodge page depends on
a lodge/ folder of accommodation pages and a much larger images
folder; dropping in the full lodge.html on its own would give you
broken links and missing photographs.


VERSION
------------------------------------------------------------------
Line 2 of every page reads:

    <!-- Eagle's Nest Resort — site simple 1.4 -->

View source on the live site to confirm what is actually deployed.
If you edit css/site.css or js/site.js, bump the ?v= number in the
<head> and at the foot of all five pages, or returning visitors
will keep seeing the old styling.
