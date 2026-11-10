import site from "./_data/site.js";

export default {
  layout: "base.njk",
  permalink: "/index.html",
  title: "Eagle's Nest Resort | Cabins, Suites & Camping on Anahim Lake, BC",
  description: "A ten-acre lakeside resort one kilometre off Highway 20 in the West Chilcotin. Suites, rooms and log cabins, a lakeside dining room, and paddling, hiking and birdwatching on the doorstep.",
  eleventyComputed: {
    jsonld: () => ({
      "@context": "https://schema.org",
      "@graph": [
        {
          "@type": "Resort",
          "@id": `${site.url}/#resort`,
          name: site.name,
          url: `${site.url}/`,
          description: "Lakeside resort on Anahim Lake in the West Chilcotin, British Columbia, with suites, rooms, log cabins and camping.",
          telephone: "+1-250-742-3707",
          email: site.email,
          image: `${site.url}/images/eagles-nest-social-preview.jpg`,
          checkinTime: "14:00",
          checkoutTime: "11:00",
          address: {
            "@type": "PostalAddress",
            streetAddress: site.address.street,
            addressLocality: site.address.locality,
            addressRegion: site.address.region,
            postalCode: site.address.postal,
            addressCountry: site.address.country,
          },
          sameAs: [site.social.facebook, site.social.instagram],
        },
        { "@type": "WebSite", "@id": `${site.url}/#website`, url: `${site.url}/`, name: site.name, inLanguage: "en-CA", publisher: { "@id": `${site.url}/#resort` } },
      ],
    }),
  },
};
