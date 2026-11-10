// Single source of truth for facts that appear on many pages. Every value here comes from the existing site.
const production = process.env.ELEVENTY_ENV === "production";
export default {
  production,
  url: "https://www.eaglesnestresort.ca",
  name: "Eagle's Nest Resort",
  place: "Anahim Lake, British Columbia",
  tagline: "West Chilcotin · British Columbia",
  phone: "250-742-3707", tel: "+12507423707", tollFree: "1-800-742-9055", tollFreeTel: "+18007429055",
  email: "info@eaglesnest-resort.com",
  address: { street: "3008 Elsey Road", locality: "Anahim Lake", region: "BC", postal: "V0L 1C0", country: "CA" },
  checkIn: "2:00 pm", checkOut: "11:00 am",
  social: {
    facebook: "https://www.facebook.com/profile.php?id=100050315986825",
    instagram: "https://www.instagram.com/eagles_nestresort",
  },
  // Pages not yet rebuilt point at the existing (legacy) pages.
  nav: [
    { label: "Stay", href: "/lodge.html", icon: "bed" },
    { label: "Things To Do", href: "/things-to-do.html", icon: "compass" },
    { label: "Getting Here", href: "/getting-here.html", icon: "route" },
    { label: "Hosts", href: "/hosts.html", icon: "people" },
  ],
  book: { label: "Book", href: "/booking.html" },
};
