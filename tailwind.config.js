/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./src/**/*.{html,js}"],
  theme: {
    extend: {
      width: {
        'login': '90%',
        'signup': '86%',
        'custom': '65%', // You can also use 'rem', 'em', etc.
        'custom-2': '35%', // Define additional custom widths as needed
      },
      height: {
        'custom': '70%', // Define custom heights
        'custom-2': '550px', // Define additional custom heights as needed
      },
    },
  },
  plugins: [],
}
