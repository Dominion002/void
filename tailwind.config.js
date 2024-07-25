/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./src/**/*.{html,js}"],
  theme: {
    extend: {
      width: {
        'login': '90%',
        'signup': '86%',
        'custom': '65%', 
        'custom-3': '70%',
        'custom-4':  '25%',
        'custom-5': '50%',      
        'custom-2': '35%', 
        'price1': '90%',
        'price2': '1%',
        'pricebox': '24.25%'
        
      },
      height: {
        'custom': '70%',
        'custom-2': '550px', 
      },
      colors: {
        customBlue: '#1DA1F2',
        customGreen: '#17BF63',
        customRed: '#E0245E',
        customme: '#306470'
      },
    },
  },
  plugins: [],
}
