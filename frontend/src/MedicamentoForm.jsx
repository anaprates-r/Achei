import { useState } from "react";

const MedicamentoForm = ({}) => {
    const [codigoMedicamento, setCodMedicamento] = useState("")
    const [nomeMedicamento,setNomeMedicamento]=  useState("")
    const [quantidade,setQuantidade]=  useState("")

    const onSubmit = async(e) => {
        e.preventDefault()

        const data = {
            codigoMedicamento,
            nomeMedicamento,
            quantidade
        }
        const url = "http://127.0.0.1:5000/create_medicamento"
        const options = {
            method: "POST",
            headers: {
                "Content-Type":"application/json"
            },
            body: JSON.stringify(data)
        }
        const response = await fetch(url,options)
        if(response.status !== 201 && response.status !== 200){
            const message = await response.json()
            alert(message.message)
        }else{
            //successfull
        }
    }

    return <form onSubmit={onSubmit}>
        <div>
            <label htmlFor="codigoMedicamento">Código do Medicamento</label>
            <input 
                type="text" 
                id="codigoMedicamento" 
                value={codigoMedicamento} 
                onChange={(e) => setCodMedicamento(e.target.value)} />
        </div>

                <div>
            <label htmlFor="nomeMedicamento">Nome do Medicamento</label>
            <input 
                type="text" 
                id="nomeMedicamento" 
                value={nomeMedicamento} 
                onChange={(e) => setNomeMedicamento(e.target.value)} />
        </div>

                <div>
            <label htmlFor="quantidade">Quantidade</label>
            <input 
                type="text" 
                id="quantidade" 
                value={quantidade} 
                onChange={(e) => setQuantidade(e.target.value)} />
        </div>
        <button type="submit"> Create Medicamento</button>
    </form>
}

export default MedicamentoForm