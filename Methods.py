from urllib.request import urlopen
import time as tt
import re


def http_fetch():
    d = str(tt.localtime()[0]) + \
        str(tt.localtime()[1] // 10) + \
        str(tt.localtime()[1])[-1] + \
        str(tt.localtime()[2] // 10) + \
        str(tt.localtime()[2] + 2)[-1]
    d = str(
        "https://cloud.timeedit.net/liu/web/schema/ri.html?h=t&sid=3&p=" + d + '-' + d + "&objects=153405.205&ox=0&types=0&fe=0&dc=f")

    with urlopen(d) as response:
        body = response.read()
        html = body.decode('utf-8')
    return html


def parse_html(html):
    indx = html.find('<div id="texttable">') - 100
    indx_1 = indx + html[indx::].find("</div>")
    target = html[indx:indx_1]

    finres = []
    holder = []

    for i in range(500):
        time = target.find("time tt")
        starget = target.find('<td  class="column')
        etarget = target.find("</td>") + 5
        catch, timecatch = target[starget:etarget], target[time:time + 50]

        if catch and holder:
            sh = target[starget:etarget - 5]
            sh = sh.find('c-1"') + len('c-1"') + 1
            res = target[starget + sh:etarget - 5]
            if (".a" not in res and ".b" not in res) and "DI1" in res:
                holder.append("DI1")
            elif "NMAA06" in res:
                holder.append("TAIU10")
            elif "Se kommentar" in res:
                tend = target.find("</tr") - 40
                tstart = target.find('c-1">') + len('c-1"') + 1
                res = target[tend + 5:tend + 40]
                res = re.search(r"([a-öA-Ö]{3,40})", res, re.IGNORECASE).group()
                holder.append({"Aktivitet": res})
            else:
                holder.append(res)
        elif timecatch:
            times = target[time + 34:time + 47]
            if holder:
                finres.append(holder[::])
                holder.clear()
            else:
                if times not in holder:
                    holder.append(times)
                etarget = time + 70
        target = target[etarget::]
    return finres


def arrange(finres):
    dagdata = {}
    j = 0
    for i in finres:
        data = {"Tid": i[0], "Kurs": i[1],
                "Typ": i[2], "Sal": i[3],
                "Lärare": i[4], "Klass": i[5]}
        try:
            if isinstance(i[2], dict):
                data["Aktivitet"] = i[2]["Aktivitet"]
                data["Typ"] = ''
        except:
            pass
        filter_data = {}
        for x in data.keys():
            if data[x] != '':
                filter_data[x] = data[x]

        dagdata[j] = filter_data
        j += 1
    # for i in range(len(dagdata)):
    #   continue
    # print(dagdata[i])

    return dagdata


def prettify_schedule(data, u_role):
    course_codes = {"TAIU10": "Analys i En Variabel"}
    response = str()

    for i in data:

        if data[i]['Klass'].lower() not in u_role: continue

        response += ' -- ' + data[i]['Tid'] + ' -- \n'
        try:
            response += "  " + data[i]['Typ'] + '\n'
        except:
            response += "  Aktivitet\n    " + data[i]['Aktivitet'] + '\n'
        try:
            if data[i]['Kurs']:
                response += "    " + data[i]['Kurs'] + f": {course_codes[data[i]['Kurs']]}" + "\n"
        except:
            pass
        try:
            if data[i]['Sal']:
                response += "      Sal: " + data[i]['Sal'] + "\n"
        except:
            pass
        try:
            if data[i]['Lärare']:
                response += "      Lärare: " + data[i]['Lärare'] + "\n"
        except:
            pass

        response += "\n"

    response = "```" + response + "```"
    return response


def get_schedule():
    a = http_fetch()
    b = parse_html(a)
    return arrange(b)


if __name__ == '__main__':
    get_schedule()
