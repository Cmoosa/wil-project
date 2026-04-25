export default {
  content: ["./index.html", "./src/**/*.{js,jsx}"],
  theme: {
    extend: {
      colors: {
        primary: "#0F62FE",
        muted: "#94A3B8",
        surface: "#F8FAFC",
        text: "#0F172A"
      },
      boxShadow: {
        DEFAULT: "0 1px 3px rgba(0,0,0,0.08)",
        card: "0 6px 18px rgba(15, 34, 58, 0.06)"
      },
      borderRadius: {
        xl: "12px"
      }
    }
  },
  plugins: []
};
