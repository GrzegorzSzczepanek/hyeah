# from xmlschema import XMLSchema
#
# form_schema = XMLSchema("../Backend/form-schema.xsd")


class N:
    def __init__(self, data, children=[]):
        self.data = data
        self.children = children

    def print(self, level=0):
        indent = "  " * level
        print(f"{indent}{self.data}")
        for child in self.children:
            child.print(level + 1)


class PCC3:
    def __init__(self):
        DataCzynnosci = {
            "name": "DataCzynnosci",
            "xml_name": "Data",
            "field_number": "P_4",
        }
        Pesel = {"name": "Pesel", "xml_name": "PESEL", "field_number": None}
        UrzadSkarbowy = {
            "name": "UrzadSkarbowy",
            "xml_name": "KodUrzedu",
            "field_number": None,
        }
        CelDeklaracji = {
            "name": "CelDeklaracji",
            "xml_name": "CelZlozenia",
            "field_number": "P_6",
        }
        Podmiot = {"name": "Podmiot", "xml_name": "Podmiot1", "field_number": "P_7"}
        RodzajPodatnika = {
            "name": "RodzajPodatnika",
            "xml_name": "rola",
            "field_number": None,
        }
        Nazwisko = {"name": "Nazwisko", "xml_name": "Nazwisko", "field_number": None}
        PierwszeImie = {
            "name": "PierwszeImie",
            "xml_name": "ImiePierwsze",
            "field_number": None,
        }
        DataUrodzenia = {
            "name": "DataUrodzenia",
            "xml_name": "DataUrodzenia",
            "field_number": None,
        }
        ImieOjca = {"name": "ImieOjca", "xml_name": None, "field_number": None}
        ImieMatki = {"name": "ImieMatki", "xml_name": None, "field_number": None}
        Kraj = {"name": "Kraj", "xml_name": "KodKraju", "field_number": None}
        Wojewodztwo = {
            "name": "Wojewodztwo",
            "xml_name": "Wojewodztwo",
            "field_number": None,
        }
        Powiat = {"name": "Powiat", "xml_name": "Powiat", "field_number": None}
        Gmina = {"name": "Gmina", "xml_name": "Gmina", "field_number": None}
        Miejscowosc = {
            "name": "Miejscowosc",
            "xml_name": "Miejscowosc",
            "field_number": None,
        }
        Ulica = {"name": "Ulica", "xml_name": "Ulica", "field_number": None}
        NrDomu = {"name": "NrDomu", "xml_name": "NrDomu", "field_number": None}
        NrLokalu = {"name": "NrLokalu", "xml_name": "NrLokalu", "field_number": None}
        KodPocztowy = {
            "name": "KodPocztowy",
            "xml_name": "KodPocztowy",
            "field_number": None,
        }
        PrzedmiotOpodatkowania = {
            "name": "PrzedmiotOpodatkowania",
            "xml_name": "P_20",
            "field_number": "P_7",
        }
        MiejscePolozeniaRzeczy = {
            "name": "MiejscePolozeniaRzeczy",
            "xml_name": None,
            "field_number": "21",
        }
        MiejsceDokonaniaCzynnosci = {
            "name": "MiejsceDokonaniaCzynnosci",
            "xml_name": None,
            "field_number": "22",
        }
        TrescCzynnosci = {
            "name": "TrescCzynnosci",
            "xml_name": "P_23",
            "field_number": "P_23",
        }
        PodstawaOpodatkowania = {
            "name": "PodstawaOpodatkowania",
            "xml_name": "P_24",
            "field_number": "P_26",
        }
        StawkaPodatku = {
            "name": "StawkaPodatku",
            "xml_name": "P_25",
            "field_number": "P_25",
        }
        ObliczonyNaleznyPodatek = {
            "name": "ObliczonyNaleznyPodatek",
            "xml_name": "P_27",
            "field_number": "P_27",
        }
        KwotaNalaznegoPodatku = {
            "name": "KwotaNalaznegoPodatku",
            "xml_name": "P_46",
            "field_number": "P_46",
        }
        KwotaPodatkuDoZaplaty = {
            "name": "KwotaPodatkuDoZaplaty",
            "xml_name": "P_53",
            "field_number": "P_53",
        }
        LiczbaDolaczonychZalacznikow = {
            "name": "LiczbaDolaczonychZalacznikow",
            "xml_name": "P_62",
            "field_number": "P_62",
        }
        Pouczenia = {"name": "Pouczenia", "xml_name": "Pouczenia", "field_number": None}

        self.form = N(
            "root",
            [
                N("SectionA", [N(DataCzynnosci), N(UrzadSkarbowy), N(CelDeklaracji)]),
                N(
                    "SectionB",
                    [
                        N(Podmiot),
                        N(RodzajPodatnika),
                        N(Pesel),
                        N(PierwszeImie),
                        N(Nazwisko),
                        N(DataUrodzenia),
                        N(ImieOjca),
                        N(ImieMatki),
                        N(Kraj),
                        N(Wojewodztwo),
                        N(Powiat),
                        N(Gmina),
                        N(Miejscowosc),
                        N(Ulica),
                        N(NrDomu),
                        N(NrLokalu),
                        N(KodPocztowy),
                    ],
                ),
                N(
                    "SectionC",
                    [
                        N(PrzedmiotOpodatkowania),
                        N(MiejscePolozeniaRzeczy),
                        N(MiejsceDokonaniaCzynnosci),
                        N(TrescCzynnosci),
                    ],
                ),
                N(
                    "SectionD",
                    [
                        N(PodstawaOpodatkowania),
                        N(StawkaPodatku),
                        N(ObliczonyNaleznyPodatek),
                        N(KwotaNalaznegoPodatku),
                    ],
                ),
                N("SectionF", [N(KwotaPodatkuDoZaplaty)]),
                N("Pouczenia", [N(Pouczenia)]),
            ],
        )
        self.form_pointer = (0, 0)

    def next(self):
        x = self.form.children[self.form_pointer[0]].children[self.form_pointer[1]]
        return x

    def increment_f_pointer(self):
        if self.form_pointer[1] + 1 < len(
            self.form.children[self.form_pointer[0]].children
        ):
            self.form_pointer = (self.form_pointer[0], self.form_pointer[1] + 1)
        else:
            if self.form_pointer[0] + 1 < len(self.form.children):
                self.form_pointer = (self.form_pointer[0] + 1, 0)
            else:
                return None
        return 1

    def fill_data(self, data):
        self.form.children[self.form_pointer[0]].children[self.form_pointer[1]].data[
            "data"
        ] = data

        if self.increment_f_pointer() == None:
            return None

        return data

    # def validate(self):
    #     return form_schema.is_valid(self.to_xml())

    def xml_gen(prev, obj):
        prev.replace("{" + obj.data["name"] + "}", obj.data["data"])

    def serialize(self):
        self.form_pointer = (0, 0)
        out = """<?xml version="1.0" encoding="UTF-8"?>
<Deklaracja xmlns="http://crd.gov.pl/wzor/2023/12/13/13064/">
    <Naglowek>
        <KodFormularza kodSystemowy="PCC-3 (6)" kodPodatku="PCC" rodzajZobowiazania="Z" wersjaSchemy="1-0E">PCC-3</KodFormularza>
        <WariantFormularza>6</WariantFormularza>
        <CelZlozenia poz="P_6">{CelDeklaracji}</CelZlozenia>
        <Data poz="P_4">{DataCzynnosci}</Data>
        <KodUrzedu>0271</KodUrzedu>
    </Naglowek>
    <Podmiot1 rola="Podatnik">
        <OsobaFizyczna>
            <PESEL>{Pesel}</PESEL>
            <ImiePierwsze>{PierwszeImie}</ImiePierwsze>
            <Nazwisko>{Nazwisko}</Nazwisko>
            <DataUrodzenia>{DataUrodzenia}</DataUrodzenia>
        </OsobaFizyczna>
        <AdresZamieszkaniaSiedziby rodzajAdresu="RAD">
            <AdresPol>
                <KodKraju>{Kraj}</KodKraju>
                <Wojewodztwo>{Wojewodztwo}</Wojewodztwo>
                <Powiat>{Powiat}</Powiat>
                <Gmina>{Gmina}</Gmina>
                <Ulica>{Ulica}</Ulica>
                <NrDomu>{NrDomu}</NrDomu>
                <NrLokalu>{NrLokalu}</NrLokalu>
                <Miejscowosc>{Miejscowosc}</Miejscowosc>
                <KodPocztowy>{KodPocztowy}</KodPocztowy>
            </AdresPol>
        </AdresZamieszkaniaSiedziby>
    </Podmiot1>
    <PozycjeSzczegolowe>
        <P_7>{Podmiot}</P_7>
        <P_20>{PrzedmiotOpodatkowania}</P_20>
        <P_21>{MiejscePolozeniaRzeczy}</P_21>
        <P_22>{MiejsceDokonaniaCzynnosci}</P_22>
        <P_23>{TrescCzynnosci}</P_23>
        <P_24>{PodstawaOpodatkowania}</P_24>
        <P_25>{StawkaPodatku}</P_25>
        <P_46>{KwotaNalaznegoPodatku}</P_46>
        <P_53>{KwotaPodatkuDoZaplaty}</P_53>
        <P_62>0</P_62>
    </PozycjeSzczegolowe>
    <Pouczenia>{Pouczenia}</Pouczenia>
 </Deklaracja>"""
        obj = self.next()
        out = out.replace("{" + obj.data["name"] + "}", obj.data["data"])
        while self.increment_f_pointer() is not None:
            obj = self.next()
            out = out.replace("{" + obj.data["name"] + "}", obj.data["data"])
        return out


form = PCC3()
while form.fill_data("dupa") is not None:
    continue

print(form.serialize())
# form.next().print()
