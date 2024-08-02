import ReactDom from "react-dom/client"
// import App from "./components/App"
import Les7 from "./components/Les7"
import './css/main.css'

const container = document.getElementById('root')
const root = ReactDom.createRoot(container)

root.render(<Les7 />)
// root.render(<App />)