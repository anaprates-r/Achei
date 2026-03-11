import React from "react"

const MedicamentoList = ({Medicamento}) => {
    return < div>
        <h2>Medicamentos</h2>

        <table>
            <thead>
                <tr>
                    <th>Estabelecimento de Saúde</th>
                    <th>Codigo do Medicamento</th>
                    <th>Nome do Medicamento</th>
                    <th>Quantidade</th>
                    <th>Ações</th>
                </tr>

            </thead>

            <tbody>
                {Medicamento.map((item) => (
                    <tr key={item.codigoMedicamento}>
                        <td>{item.estabelecimentoSaude}</td>
                        <td>{item.codigoMedicamento}</td>
                        <td>{item.nomeMedicamento}</td>
                        <td>{item.quantidade}</td>
                        <td> 
                            <button onClick={''} >Update</button>
                            <button>Delete</button>
                        </td>
                    </tr>
                ))}
                
            </tbody>
        </table>
    
    </div>
}

export default MedicamentoList