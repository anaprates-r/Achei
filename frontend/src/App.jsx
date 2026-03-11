import { useState,useEffect } from 'react'
import MedicamentoList from './MedicamentoList' 
// import MedicamentoForm from './MedicamentoForm'
import UploadFile from './upload'
import './App.css'

function App() {
  const [Medicamento, setMedicamento] = useState([])
  

  useEffect(() => {
    fetchMedicamento()
  }, [])

  const fetchMedicamento = async () => {
    const response = await fetch("http://127.0.0.1:5000/medicamento")
    const data = await response.json()
    setMedicamento(data.Medicamento)
    console.log(data.Medicamento)
  }

  return <>
    <MedicamentoList Medicamento={Medicamento}/>
    {/* <MedicamentoForm/> */}
    <UploadFile/>
  </>
}

export default App
