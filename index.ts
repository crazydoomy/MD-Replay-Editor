import "frida-il2cpp-bridge";

Il2Cpp.perform(() => {
    const il2cpplib = Il2Cpp.Domain.assemblies["Assembly-CSharp"].image;
    const mscorlib = Il2Cpp.Domain.assemblies["mscorlib"].image;
    const SystemBytes =  mscorlib.classes["System.Byte"];
    const deserializeAsync = il2cpplib.classes["YgomSystem.Network.FormatYgom"].methods.DeserializeAsync;
    const getpubliclevel = il2cpplib.classes["YgomGame.Duel.Util"].methods.GetPublicLevel;
    console.log("attached")
    deserializeAsync.implementation = function (ba : Il2Cpp.Array<number>, onfinish : Il2Cpp.Object) : void {
        var array = [];
        for (let i = 0; i < ba.length; i++){
            array.push(ba.get(i));
        }
        //convert to buffer -> b64
        var u8array = new Uint8Array(array);
        var hexencoded = Buffer.from(u8array).toString('hex');
        if (hexencoded.includes("7265706c61796d")) { //replaym in b64
            //send to python program and wait for response
            send(hexencoded);
            recv(function (obj) {
                hexencoded = obj.replay;
            }).wait();
            //replace with new
            var b64decoded = Buffer.from(hexencoded, 'hex');
            var newarray = [];
            for (let i = 0; i<b64decoded.length; i++) {
                newarray.push(b64decoded[i]);
            }

            ba = Il2Cpp.Array.from(SystemBytes, newarray);
            this.methods.DeserializeAsync.invoke(ba, onfinish);
        } else {
            this.methods.DeserializeAsync.invoke(ba, onfinish);
        }
    }
    getpubliclevel.implementation = function() {
        var a = getpubliclevel.invoke<Il2Cpp.Object>()
        a.fields["value__"].value = 2
        return a
    }
});
