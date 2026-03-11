import { useState } from "react"

const UploadFile = () => {
  const [file, setFile] = useState(null)

  const onFileChange = (e) => {
    // Access the first file from the input's file list
    setFile(e.target.files[0])
  }

  const onSubmit = async (e) => {
    e.preventDefault()
    if (!file) return alert("Please select a file first!")

    const url = "http://127.0.0.1:5000/upload"

    // 1. Create a FormData object
    const formData = new FormData()
    // 2. Append the file (matching the key your backend expects)
    formData.append("file", file)

    const options = {
      method: "POST",
      body: formData,
    }

    try {
      const response = await fetch(url, options)
      const data = await response.json()

      if (response.status !== 201 && response.status !== 200) {
        alert(data.message || "Upload failed")
      } else {
        alert("File uploaded successfully!")
      }
    } catch (error) {
      console.error("Error uploading file:", error)
    }
  }

  return <div>
    <p> Atualize o banco de daos</p>
        <form onSubmit={onSubmit}>
      <label htmlFor="file">Selecione um arquivo</label>
      <input type="file" name="file" id="file" onChange={onFileChange} />
      <input type="submit" value="upload" />
    </form>
  </div>

}

export default UploadFile
