import ReactDom from "react-dom/client"
import AppRoute from './components/AppRoute'
import './css/main.css'
// import App from "./components/App"
//import Les7 from "./components/Les7"


const container = document.getElementById('root')
const root = ReactDom.createRoot(container)

root.render(<AppRoute />)
//root.render(<Les7 />)
// root.render(<App />)