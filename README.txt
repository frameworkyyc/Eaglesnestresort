EAGLE'S NEST RESORT — LIVE SITE (site live 3.1)
==================================================================
The version that goes on the live domain. Pages are switched on
as they are finished.


WHAT TO UPLOAD
------------------------------------------------------------------
Upload everything in this folder to the root of your web host,
keeping the structure as it is:

    index.html            The home page — the real thing
    lodge.html            Accommodations + resort gallery
    lodge/                11 accommodation pages
    hosts.html            Your Hosts — finished
    booking.html          Booking — contact form and options
    getting-here.html     Getting Here — finished
    things-to-do.html     "Coming soon"
    hosts.html            "Coming soon"

    css/site.css
    js/site.js
    images/               26 files
    images/gal/           67 gallery thumbnails
    images/lg/            67 larger versions for the viewer
    _headers              cache rules (Netlify; harmless elsewhere)

21 MB in total. Delete this README before going live if you like.


HOW IT BEHAVES
------------------------------------------------------------------
- The HOME PAGE is complete. Hero, the Highway 20 map, the lodge
  carousel, the hosts introduction, the two guest reviews, and the
  closing call to action.

- THE LODGE now offers two paths at the top: view the resort
  (jumps to the gallery and opens it) or find a place to stay
  (jumps to the accommodations).

  WHERE TO STAY lists 12 entries — 7 suites, 4 cabins and
  camping — filterable by guests, type and power. Each card links
  to its own page at lodge/<name>.html.

  All twelve now have their own photographs. No placeholders
  remain.

  No prices are shown anywhere public. The rates are still in the
  data (build/stays_live.py) for when you want them back.

  The resort gallery sits below. Collapsed, it is the full masonry
  gallery at its normal size, simply cropped after roughly its
  first row by a wrapper (.gal-clip) with a gradient easing the
  cut. VIEW FULL GALLERY lifts the crop to show all 34.

- YOUR HOSTS is the finished page: Diane, Murray and Oliver, and
  the two guest reviews.

- GETTING HERE is the finished page: the four ways in, the aerial
  of the property, the float plane at the dock, and the contact
  and arrival details.

- THINGS TO DO is now a full page: paddling and fishing from the
  dock, birds, the waterfalls, hiking, a turn into winter, dark
  skies, and a closing call to Diane and Murray. Seven photographs are still to come and
  show a neutral frame until they arrive.

- BOOKING is a page of its own now: phone and email, an enquiry
  form, and the online options. Both the Expedia and Booking.com
  listings link out in a new tab.


ADDING PHOTOGRAPHS TO AN ACCOMMODATION
------------------------------------------------------------------
Every accommodation now has its own photographs. No placeholders
remain. NO accommodation
borrows another one's photographs — that is deliberate.

Send me a batch and say which suite or cabin it belongs to, and it
gets attached to that one only: card, hero and its own gallery.

Note on the heritage photographs already on the site: they were
supplied as "the heritage cabins" together. Most are now placed —
heritage-cabin is Heritage 2, matched to its own batch. The
lakefront frame is the one still in doubt; see HANDOVER.txt.


STILL TO CONFIRM
------------------------------------------------------------------
  - TWO HELD PHOTOGRAPHS. One from the Pine batch and one from the
    Pelican batch were not published because they contradict the
    written specification (see HANDOVER.txt). They have not been
    assigned to any other room.
  - TV. The old site copy claimed satellite TV for "suites" as a
    group, but the owners have confirmed Pine and Pelican have
    none. That makes the old group claim unreliable, so no TV is
    listed for ANY accommodation. Tell me which of Den, Chilcotin,
    Tucson, Blue Heron and Green actually have one.
  - Camping: number of sites, hookups, facilities, occupancy and
    whether trailers are welcome. One Camping entry exists with a
    photograph and no invented detail.
  - Whether the cabins have Wi-Fi. Only the suites are listed
    with it, as instructed.
  - info@eaglesnest-resort.com — still unverified.


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


HOW THE ENQUIRY FORM WORKS
------------------------------------------------------------------
Cloudflare Pages serves files; it does not process form posts. So
by default, pressing Send opens the visitor's email app with all
their answers already written into a message addressed to you.
They press send there and it arrives as a normal email. This needs
no account, no keys and no backend, and it works on every host.

The form says so plainly underneath, so nobody is misled into
thinking they have sent something when they have not.

IMPORTANT: it sends to info@eaglesnest-resort.com. That address
was never confirmed. Check it works before this page goes live —
if it is wrong, every enquiry bounces. Search booking.html for
data-mailto to change it.

WANT PROPER FORM SUBMISSIONS INSTEAD?
Sign up for a form service that accepts posts from a static site
(Web3Forms and Formspree both have free tiers), then in
booking.html find:

    data-endpoint=""

and paste your endpoint URL between the quotes. That is the only
change needed. The form will then post directly, show a thank-you
message in the page, and clear itself — and if the service is ever
down it falls back to the email method rather than losing the
message. A hidden anti-spam field is already in place.


CHANGING THE LISTING LINKS
------------------------------------------------------------------
Both live on booking.html only. Search it for:

    expedia.ca/Anahim-Lake-Hotels
    booking.com/hotel/ca/anahim-lake

and replace the whole href. Both open in a new tab via
target="_blank" rel="noopener noreferrer" — keep those attributes.

Use the plain listing address, not a link copied out of a search
results page. Those carry the dates you happened to search for and
a pile of tracking parameters, which would pin every visitor to
your search instead of their own.


PHOTOGRAPHS STILL NEEDED — THINGS TO DO
------------------------------------------------------------------
Three frames on that page show a neutral holder naming what belongs
there, all of them in the winter section. Nothing has been filled
with an unrelated photograph.

    snowmobiling    ice fishing    skating on the lake

Beef Trail Falls has a photograph of the canyon on the way in, but
not of the falls themselves. The winter section opens with a
full-width plate of the lodge across the frozen lake; the three
activity frames beneath it are the ones still waiting.

Drop each one in and swap the holder for an <img>; the layout does
not change.

IF THE SITE LOOKS UNSTYLED AFTER A DEPLOY
------------------------------------------------------------------
That is almost always an old stylesheet still being served, not
broken CSS. To check:

1. View source on the live page and find the line:
       <link rel="stylesheet" href="css/site.css?v=81d61dd6">
   The number must match the one recorded in HANDOVER.txt.
2. Open that css URL directly in the browser and search it for
       .accom
   If it is not there, the stylesheet on the server is out of date
   and css/site.css did not upload.

Upload the WHOLE folder every time, not just the .html files. The
css, js and images folders must go up together.

The ?v= number now tracks this build, so every release changes the
address of the stylesheet and browsers are forced to fetch it
fresh. _headers also tells Cloudflare to revalidate css and js on
every request.


VERSION
------------------------------------------------------------------
Line 2 of every page reads:

    <!-- Eagle's Nest Resort — site live 3.1 -->

That marker is re-synced only on a full export, so it reads as the
release a page was last fully shipped in. The current release
number is in HANDOVER.txt. View source on the live site to confirm
what is actually deployed.
If you edit css/site.css or js/site.js, bump the ?v= number on all
18 pages, or returning visitors will keep seeing the old styling.
