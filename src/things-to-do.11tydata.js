import site from "./_data/site.js";

const url = `${site.url}/things-to-do`;

// Places named on the page. Descriptions are the existing site's own words.
const places = [
  { name: "Rainbow Range", description: "Old volcanic rock streaked red, orange and yellow, west along Highway 20 inside Tweedsmuir Park." },
  { name: "Hunlen Falls", description: "Farther into Tweedsmuir Park, and a longer day than the others." },
  { name: "Hotnarko Falls", description: "The Hotnarko River drops off the edge of the Precipice, a canyon walled in basalt." },
];

export default {
  layout: "legacy-shell.njk",
  permalink: "/things-to-do.html",
  title: "Things To Do Near Anahim Lake | Eagle's Nest Resort, West Chilcotin BC",
  description: "Paddling, fishing and birdwatching from the dock at Anahim Lake, waterfalls and trails through the West Chilcotin, and a lake that freezes hard enough to skate.",
  canonical: url,
  jsonld: {
    "@context": "https://schema.org",
    "@graph": [
      {
        "@type": "BreadcrumbList",
        itemListElement: [
          { "@type": "ListItem", position: 1, name: "Home", item: `${site.url}/` },
          { "@type": "ListItem", position: 2, name: "Things To Do", item: url },
        ],
      },
      {
        "@type": "WebPage",
        "@id": `${url}#page`,
        url,
        name: "Things to do near Anahim Lake",
        about: { "@id": `${site.url}/#resort` },
        mainEntity: {
          "@type": "ItemList",
          itemListElement: places.map((p, i) => ({
            "@type": "ListItem",
            position: i + 1,
            item: { "@type": "TouristAttraction", name: p.name, description: p.description },
          })),
        },
      },
      {
        "@type": "Resort",
        "@id": `${site.url}/#resort`,
        name: site.name,
        url: `${site.url}/`,
        telephone: "+1-250-742-3707",
        address: {
          "@type": "PostalAddress",
          streetAddress: site.address.street,
          addressLocality: site.address.locality,
          addressRegion: site.address.region,
          postalCode: site.address.postal,
          addressCountry: site.address.country,
        },
      },
    ],
  },
};
