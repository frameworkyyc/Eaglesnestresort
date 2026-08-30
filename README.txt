EAGLE'S NEST RESORT — LIVE SITE (site live 1.7)
==================================================================
The version that goes on the live domain. Pages are switched on
as they are finished.


WHAT TO UPLOAD
------------------------------------------------------------------
Upload everything in this folder to the root of your web host,
keeping the structure as it is:

    index.html            The home page — the real thing
    lodge.html            A gallery of the property
    hosts.html            Your Hosts — finished
    booking.html          Booking — contact form and options
    getting-here.html     Getting Here — finished
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

- YOUR HOSTS is the finished page: Diane, Murray and Oliver, and
  the two guest reviews.

- GETTING HERE is the finished page: the four ways in, the aerial
  of the property, the float plane at the dock, and the contact
  and arrival details.

- THINGS TO DO is the one page still to come. It opens a real page
  saying so, with your phone number, email address and address on
  it. Nobody hits a dead link or a 404.

- BOOKING is a page of its own now: phone and email, an enquiry
  form, and the online options. The Booking.com listing links out
  in a new tab. Expedia is a labelled placeholder until you send
  me that URL.


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


CHANGING THE BOOKING LINK
------------------------------------------------------------------
The Booking.com URL appears several times. To change it, search
every .html file for:

    booking.com/hotel/ca/anahim-lake

and replace the whole href. It opens in a new tab via
target="_blank" rel="noopener noreferrer" — keep those attributes.


TURNING THE LAST PAGE ON
------------------------------------------------------------------
The finished Things To Do page already exists in the full build.
When you want it live, replace things-to-do.html with the real one
and upload the extra images it needs.

Do not mix the two builds halfway. The full Lodge page depends on
a lodge/ folder of accommodation pages and a much larger images
folder; dropping in the full lodge.html on its own would give you
broken links and missing photographs.


VERSION
------------------------------------------------------------------
Line 2 of every page reads:

    <!-- Eagle's Nest Resort — site live 1.7 -->

View source on the live site to confirm what is actually deployed.
If you edit css/site.css or js/site.js, bump the ?v= number in the
<head> and at the foot of all five pages, or returning visitors
will keep seeing the old styling.
