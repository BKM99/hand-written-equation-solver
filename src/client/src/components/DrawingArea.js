import { useRef, useState, useEffect, useCallback } from 'react'
import axios from 'axios'

const DrawingArea = () => {
    const canvasRef = useRef(null)
    const ctx = useRef(null)
    const [mouseDown, setMouseDown] = useState(false)
    const [lastPosition, setPosition] = useState({
        x: 0,
        y: 0
    })

    var [result, setResult] = useState('waiting for result...')

    useEffect(() => {
        if (canvasRef.current) {
            ctx.current = canvasRef.current.getContext('2d', {alpha: true})
            ctx.current.fillStyle = "#FFF"
            ctx.current.fillRect(0, 0, ctx.current.width, ctx.current.height)
        }
    }, [])

    const draw = useCallback((x, y) => {
        if (mouseDown) {
            ctx.current = canvasRef.current.getContext('2d', {alpha: false})
            ctx.current.beginPath()
            ctx.current.strokeStyle = 'black'
            ctx.current.lineWidth = 5
            ctx.current.lineJoin = 'round'
            ctx.current.moveTo(lastPosition.x, lastPosition.y)
            ctx.current.lineTo(x, y)
            ctx.current.closePath()
            ctx.current.stroke()

            setPosition({
                x,
                y
            })
        }

    }, [lastPosition, mouseDown, setPosition])

    const onMouseDown = (e) => {
        setPosition({
            x: e.pageX,
            y: e.pageY
        })
        setMouseDown(true)
    }

    const onMouseUp = (e) => {
        setMouseDown(false)
    }

    const onMouseMove = (e) => {
        draw(e.pageX, e.pageY)
    }

    const clear = () => {
        ctx.current.clearRect(0, 0, ctx.current.canvas.width, ctx.current.canvas.height)
        setResult('')
    }

    const saveImage = async () => {
        changeNonOpaque()
        const image = canvasRef.current.toDataURL();
        console.log(image)

        // const blob = await (await fetch(image)).blob();
        // const blobURL = URL.createObjectURL(blob);
        // const link = document.createElement('a');
        // link.href = blobURL;
        // link.download = "image.png";
        // link.click();

        const dataToSend = {
            imageData: image
        }
        console.log(dataToSend)
        const data = JSON.stringify(dataToSend)
        console.log(data.length)

        axios.post('http://127.0.0.1:8000/api/data', data)
            .then(function(response) {
                console.log(response.data)
                result = JSON.stringify(response.data.result)
                setResult(result)
            })
            .catch(function(error) {
                console.log(error)
            })

    }

    const changeNonOpaque = () => {
        // change non-opaque pixels to white
        var imgData=ctx.current.getImageData(0,0,ctx.current.canvas.width,ctx.current.canvas.height);
        var data=imgData.data;
        for(var i=0;i<data.length;i+=4){
            if(data[i+3]<255){
                data[i]=255;
                data[i+1]=255;
                data[i+2]=255;
                data[i+3]=255;
            }
        }
        ctx.current.putImageData(imgData,0,0);
    }

    return (
        <div>
            <canvas
                style={{
                    border: "2px solid #000",
                }}
                width={800}
                height={450}
                ref={canvasRef}
                onMouseDown={onMouseDown}
                onMouseUp={onMouseUp}
                onMouseLeave={onMouseUp}
                onMouseMove={onMouseMove}
                />
            <div>
                <button onClick={clear}>Clear</button>
                <button onClick={saveImage}>Solve</button>
            </div>
                <h2>
                Answer: {result}
            </h2>
        </div>
    )
}

export default DrawingArea
