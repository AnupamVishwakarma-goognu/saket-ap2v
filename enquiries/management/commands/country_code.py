from django.core.management.base import BaseCommand, CommandError
from core.models import CountryCode


class Command(BaseCommand):
    help = 'Add country Code and Dialing code'

    def handle(self, *args, **kwargs):
        all_code = [  
            {
                "country": "Afghanistan",
                "country_code": "AF",
                "dialing_code": "+93"
            },  
            {
                "country": "Albania",
                "country_code": "AL",
                "dialing_code": "+355"
            },  
            {
                "country": "Algeria",
                "country_code": "DZ",
                "dialing_code": "+213"
            },  
            {
                "country": "American Samoa",
                "country_code": "AS",
                "dialing_code": "-683"
            },  
            {
                "country": "Andorra, Principality",
                "country_code": "AD",
                "dialing_code": "+376"
            },  
            {
                "country": "Angola",
                "country_code": "AO",
                "dialing_code": "+244"
            },  
            {
                "country": "Anguilla",
                "country_code": "AI",
                "dialing_code": "-263"
            },  
            {
                "country": "Antarctica",
                "country_code": "AQ",
                "dialing_code": "+672"
            },  
            {
                "country": "Antigua and Barbuda",
                "country_code": "AG",
                "dialing_code": "-267"
            },  
            {
                "country": "Argentina",
                "country_code": "AR",
                "dialing_code": "+54"
            },  
            {
                "country": "Armenia",
                "country_code": "AM",
                "dialing_code": "+374"
            },  
            {
                "country": "Aruba",
                "country_code": "AW",
                "dialing_code": "+297"
            },  
            {
                "country": "Australia",
                "country_code": "AU",
                "dialing_code": "+61"
            },  
            {
                "country": "Austria",
                "country_code": "AT",
                "dialing_code": "+43"
            },  
            {
                "country": "Azerbaijan or Azerbaidjan",
                "country_code": "AZ",
                "dialing_code": "+994"
            },  
            {
                "country": "Bahamas",
                "country_code": "BS",
                "dialing_code": "-241"
            },  
            {
                "country": "Bahrain, Kingdom",
                "country_code": "BH",
                "dialing_code": "+973"
            },  
            {
                "country": "Bangladesh",
                "country_code": "BD",
                "dialing_code": "+880"
            },  
            {
                "country": "Barbados",
                "country_code": "BB",
                "dialing_code": "-245"
            },  
            {
                "country": "Belarus",
                "country_code": "BY",
                "dialing_code": "+375"
            },  
            {
                "country": "Belgium",
                "country_code": "BE",
                "dialing_code": "+32"
            },  
            {
                "country": "Belize",
                "country_code": "BZ",
                "dialing_code": "+501"
            },  
            {
                "country": "Benin",
                "country_code": "BJ",
                "dialing_code": "+229"
            },  
            {
                "country": "Bermuda",
                "country_code": "BM",
                "dialing_code": "-440"
            },  
            {
                "country": "Bhutan, Kingdom",
                "country_code": "BT",
                "dialing_code": "+975"
            },  
            {
                "country": "Bolivia",
                "country_code": "BO",
                "dialing_code": "+591"
            },  
            {
                "country": "Bosnia and Herzegovina",
                "country_code": "BA",
                "dialing_code": "+387"
            },  
            {
                "country": "Botswana",
                "country_code": "BW",
                "dialing_code": "+267"
            },  
            {
                "country": "Bouvet Island",
                "country_code": "BV",
                "dialing_code": ""
            },  
            {
                "country": "Brazil",
                "country_code": "BR",
                "dialing_code": "+55"
            },  
            {
                "country": "British Indian Ocean Territory",
                "country_code": "IO",
                "dialing_code": ""
            },  
            {
                "country": "Brunei",
                "country_code": "BN",
                "dialing_code": "+673"
            },  
            {
                "country": "Bulgaria",
                "country_code": "BG",
                "dialing_code": "+359"
            },  
            {
                "country": "Burkina Faso",
                "country_code": "BF",
                "dialing_code": "+226"
            },  
            {
                "country": "Burundi",
                "country_code": "BI",
                "dialing_code": "+257"
            },  
            {
                "country": "Cambodia, Kingdom",
                "country_code": "KH",
                "dialing_code": "+855"
            },  
            {
                "country": "Cameroon",
                "country_code": "CM",
                "dialing_code": "+237"
            },  
            {
                "country": "Canada",
                "country_code": "CA",
                "dialing_code": "+1"
            },  
            {
                "country": "Cape Verde",
                "country_code": "CV",
                "dialing_code": "+238"
            },  
            {
                "country": "Cayman Islands",
                "country_code": "KY",
                "dialing_code": "-344"
            },  
            {
                "country": "Central African Republic",
                "country_code": "CF",
                "dialing_code": "+236"
            },  
            {
                "country": "Chad",
                "country_code": "TD",
                "dialing_code": "+235"
            },  
            {
                "country": "Chile",
                "country_code": "CL",
                "dialing_code": "+56"
            },  
            {
                "country": "China",
                "country_code": "CN",
                "dialing_code": "+86"
            },  
            {
                "country": "Christmas Island",
                "country_code": "CX",
                "dialing_code": "+53"
            },  
            {
                "country": "Cocos",
                "country_code": "CC",
                "dialing_code": "+61"
            },  
            {
                "country": "Colombia",
                "country_code": "CO",
                "dialing_code": "+57"
            },  
            {
                "country": "Comoros",
                "country_code": "KM",
                "dialing_code": "+269"
            },  
            {
                "country": "Congo, Democratic Republic",
                "country_code": "CD",
                "dialing_code": "+243"
            },  
            {
                "country": "Congo, Republic",
                "country_code": "CG",
                "dialing_code": "+242"
            },  
            {
                "country": "Cook Islands",
                "country_code": "CK",
                "dialing_code": "+682"
            },  
            {
                "country": "Costa Rica",
                "country_code": "CR",
                "dialing_code": "+506"
            },  
            {
                "country": "Cote D'Ivoire",
                "country_code": "CI",
                "dialing_code": "+225"
            },  
            {
                "country": "Croatia",
                "country_code": "HR",
                "dialing_code": "+385"
            },  
            {
                "country": "Cuba",
                "country_code": "CU",
                "dialing_code": "+53"
            },  
            {
                "country": "Cyprus",
                "country_code": "CY",
                "dialing_code": "+357"
            },  
            {
                "country": "Czech Republic",
                "country_code": "CZ",
                "dialing_code": "+420"
            },  
            {
                "country": "Czechoslavakia",
                "country_code": "CS",
                "dialing_code": ""
            },  
            {
                "country": "Denmark",
                "country_code": "DK",
                "dialing_code": "+45"
            },  
            {
                "country": "Djibouti",
                "country_code": "DJ",
                "dialing_code": "+253"
            },  
            {
                "country": "Dominica",
                "country_code": "DM",
                "dialing_code": "-766"
            },  
            {
                "country": "Dominican Republic",
                "country_code": "DO",
                "dialing_code": "+1"
            },  
            {
                "country": "East Timor",
                "country_code": "TP",
                "dialing_code": "+670"
            },  
            {
                "country": "Ecuador",
                "country_code": "EC",
                "dialing_code": "+593"
            },  
            {
                "country": "Egypt",
                "country_code": "EG",
                "dialing_code": "+20"
            },  
            {
                "country": "El Salvador",
                "country_code": "SV",
                "dialing_code": "+503"
            },  
            {
                "country": "Equatorial Guinea",
                "country_code": "GQ",
                "dialing_code": "+240"
            },  
            {
                "country": "Eritrea",
                "country_code": "ER",
                "dialing_code": "+291"
            },  
            {
                "country": "Estonia",
                "country_code": "EE",
                "dialing_code": "+372"
            },  
            {
                "country": "Ethiopia",
                "country_code": "ET",
                "dialing_code": "+251"
            },  
            {
                "country": "Falkland Islands",
                "country_code": "FK",
                "dialing_code": "+500"
            },  
            {
                "country": "Faroe Islands",
                "country_code": "FO",
                "dialing_code": "+298"
            },  
            {
                "country": "Fiji",
                "country_code": "FJ",
                "dialing_code": "+679"
            },  
            {
                "country": "Finland",
                "country_code": "FI",
                "dialing_code": "+358"
            },  
            {
                "country": "France",
                "country_code": "FR",
                "dialing_code": "+33"
            },  
            {
                "country": "French Guiana or French Guyana",
                "country_code": "GF",
                "dialing_code": "+594"
            },  
            {
                "country": "French Polynesia",
                "country_code": "PF",
                "dialing_code": "+689"
            },  
            {
                "country": "French Southern Territories and Antarctic Lands",
                "country_code": "TF",
                "dialing_code": ""
            },  
            {
                "country": "Gabon",
                "country_code": "GA",
                "dialing_code": "+241"
            },  
            {
                "country": "Gambia, The",
                "country_code": "GM",
                "dialing_code": "+220"
            },  
            {
                "country": "Georgia",
                "country_code": "GE",
                "dialing_code": "+995"
            },  
            {
                "country": "Germany",
                "country_code": "DE",
                "dialing_code": "+49"
            },  
            {
                "country": "Ghana",
                "country_code": "GH",
                "dialing_code": "+233"
            },  
            {
                "country": "Gibraltar",
                "country_code": "GI",
                "dialing_code": "+350"
            },  
            {
                "country": "Great Britain",
                "country_code": "GB",
                "dialing_code": ""
            },  
            {
                "country": "Greece",
                "country_code": "GR",
                "dialing_code": "+30"
            },  
            {
                "country": "Greenland",
                "country_code": "GL",
                "dialing_code": "+299"
            },  
            {
                "country": "Grenada",
                "country_code": "GD",
                "dialing_code": "-472"
            },  
            {
                "country": "Guadeloupe",
                "country_code": "GP",
                "dialing_code": "+590"
            },  
            {
                "country": "Guam",
                "country_code": "GU",
                "dialing_code": "-670"
            },  
            {
                "country": "Guatemala",
                "country_code": "GT",
                "dialing_code": "+502"
            },  
            {
                "country": "Guinea",
                "country_code": "GN",
                "dialing_code": "+224"
            },  
            {
                "country": "Guinea-Bissau",
                "country_code": "GW",
                "dialing_code": "+245"
            },  
            {
                "country": "Guyana",
                "country_code": "GY",
                "dialing_code": "+592"
            },  
            {
                "country": "Haiti",
                "country_code": "HT",
                "dialing_code": "+509"
            },  
            {
                "country": "Heard Island and McDonald Islands",
                "country_code": "HM",
                "dialing_code": ""
            },  
            {
                "country": "Holy See",
                "country_code": "VA",
                "dialing_code": ""
            },  
            {
                "country": "Honduras",
                "country_code": "HN",
                "dialing_code": "+504"
            },  
            {
                "country": "Hong Kong",
                "country_code": "HK",
                "dialing_code": "+852"
            },  
            {
                "country": "Hungary",
                "country_code": "HU",
                "dialing_code": "+36"
            },  
            {
                "country": "Iceland",
                "country_code": "IS",
                "dialing_code": "+354"
            },  
            {
                "country": "India",
                "country_code": "IN",
                "dialing_code": "+91"
            },  
            {
                "country": "Indonesia",
                "country_code": "ID",
                "dialing_code": "+62"
            },  
            {
                "country": "Iran, Islamic Republic",
                "country_code": "IR",
                "dialing_code": "+98"
            },  
            {
                "country": "Iraq",
                "country_code": "IQ",
                "dialing_code": "+964"
            },  
            {
                "country": "Ireland",
                "country_code": "IE",
                "dialing_code": "+353"
            },  
            {
                "country": "Israel",
                "country_code": "IL",
                "dialing_code": "+972"
            },  
            {
                "country": "Italy",
                "country_code": "IT",
                "dialing_code": "+39"
            },  
            {
                "country": "Jamaica",
                "country_code": "JM",
                "dialing_code": "-875"
            },  
            {
                "country": "Japan",
                "country_code": "JP",
                "dialing_code": "+81"
            },  
            {
                "country": "Jordan",
                "country_code": "JO",
                "dialing_code": "+962"
            },  
            {
                "country": "Kazakstan or Kazakhstan",
                "country_code": "KZ",
                "dialing_code": "+7"
            },  
            {
                "country": "Kenya",
                "country_code": "KE",
                "dialing_code": "+254"
            },  
            {
                "country": "Kiribati",
                "country_code": "KI",
                "dialing_code": "+686"
            },  
            {
                "country": "Korea, Democratic People's Republic",
                "country_code": "KP",
                "dialing_code": "+850"
            },  
            {
                "country": "Korea, Republic",
                "country_code": "KR",
                "dialing_code": "+82"
            },  
            {
                "country": "Kuwait",
                "country_code": "KW",
                "dialing_code": "+965"
            },  
            {
                "country": "Kyrgyzstan",
                "country_code": "KG",
                "dialing_code": "+996"
            },  
            {
                "country": "Lao People's Democratic Republic",
                "country_code": "LA",
                "dialing_code": "+856"
            },  
            {
                "country": "Latvia",
                "country_code": "LV",
                "dialing_code": "+371"
            },  
            {
                "country": "Lebanon",
                "country_code": "LB",
                "dialing_code": "+961"
            },  
            {
                "country": "Lesotho",
                "country_code": "LS",
                "dialing_code": "+266"
            },  
            {
                "country": "Liberia",
                "country_code": "LR",
                "dialing_code": "+231"
            },  
            {
                "country": "Libya",
                "country_code": "LY",
                "dialing_code": "+218"
            },  
            {
                "country": "Liechtenstein",
                "country_code": "LI",
                "dialing_code": "+423"
            },  
            {
                "country": "Lithuania",
                "country_code": "LT",
                "dialing_code": "+370"
            },  
            {
                "country": "Luxembourg",
                "country_code": "LU",
                "dialing_code": "+352"
            },  
            {
                "country": "Macau",
                "country_code": "MO",
                "dialing_code": "+853"
            },  
            {
                "country": "Macedonia, The Former Yugoslav Republic",
                "country_code": "MK",
                "dialing_code": "+389"
            },  
            {
                "country": "Madagascar",
                "country_code": "MG",
                "dialing_code": "+261"
            },  
            {
                "country": "Malawi",
                "country_code": "MW",
                "dialing_code": "+265"
            },  
            {
                "country": "Malaysia",
                "country_code": "MY",
                "dialing_code": "+60"
            },  
            {
                "country": "Maldives",
                "country_code": "MV",
                "dialing_code": "+960"
            },  
            {
                "country": "Mali",
                "country_code": "ML",
                "dialing_code": "+223"
            },  
            {
                "country": "Malta",
                "country_code": "MT",
                "dialing_code": "+356"
            },  
            {
                "country": "Marshall Islands",
                "country_code": "MH",
                "dialing_code": "+692"
            },  
            {
                "country": "Martinique",
                "country_code": "MQ",
                "dialing_code": "+596"
            },  
            {
                "country": "Mauritania",
                "country_code": "MR",
                "dialing_code": "+222"
            },  
            {
                "country": "Mauritius",
                "country_code": "MU",
                "dialing_code": "+230"
            },  
            {
                "country": "Mayotte",
                "country_code": "YT",
                "dialing_code": "+269"
            },  
            {
                "country": "Mexico",
                "country_code": "MX",
                "dialing_code": "+52"
            },  
            {
                "country": "Micronesia, Federated States",
                "country_code": "FM",
                "dialing_code": "+691"
            },  
            {
                "country": "Moldova, Republic",
                "country_code": "MD",
                "dialing_code": "+373"
            },  
            {
                "country": "Monaco, Principality",
                "country_code": "MC",
                "dialing_code": "+377"
            },  
            {
                "country": "Mongolia",
                "country_code": "MN",
                "dialing_code": "+976"
            },  
            {
                "country": "Montserrat",
                "country_code": "MS",
                "dialing_code": "-663"
            },  
            {
                "country": "Morocco",
                "country_code": "MA",
                "dialing_code": "+212"
            },  
            {
                "country": "Mozambique",
                "country_code": "MZ",
                "dialing_code": "+258"
            },  
            {
                "country": "Myanmar, Union",
                "country_code": "MM",
                "dialing_code": "+95"
            },  
            {
                "country": "Namibia",
                "country_code": "NA",
                "dialing_code": "+264"
            },  
            {
                "country": "Nauru",
                "country_code": "NR",
                "dialing_code": "+674"
            },  
            {
                "country": "Nepal",
                "country_code": "NP",
                "dialing_code": "+977"
            },  
            {
                "country": "Netherlands",
                "country_code": "NL",
                "dialing_code": "+31"
            },  
            {
                "country": "Netherlands Antilles",
                "country_code": "AN",
                "dialing_code": "+599"
            },  
            {
                "country": "New Caledonia",
                "country_code": "NC",
                "dialing_code": "+687"
            },  
            {
                "country": "New Zealand",
                "country_code": "NZ",
                "dialing_code": "+64"
            },  
            {
                "country": "Nicaragua",
                "country_code": "NI",
                "dialing_code": "+505"
            },  
            {
                "country": "Niger",
                "country_code": "NE",
                "dialing_code": "+227"
            },  
            {
                "country": "Nigeria",
                "country_code": "NG",
                "dialing_code": "+234"
            },  
            {
                "country": "Niue",
                "country_code": "NU",
                "dialing_code": "+683"
            },  
            {
                "country": "Norfolk Island",
                "country_code": "NF",
                "dialing_code": "+672"
            },  
            {
                "country": "Northern Mariana Islands",
                "country_code": "MP",
                "dialing_code": "-669"
            },  
            {
                "country": "Norway",
                "country_code": "NO",
                "dialing_code": "+47"
            },  
            {
                "country": "Oman, Sultanate",
                "country_code": "OM",
                "dialing_code": "+968"
            },  
            {
                "country": "Pakistan",
                "country_code": "PK",
                "dialing_code": "+92"
            },  
            {
                "country": "Palau",
                "country_code": "PW",
                "dialing_code": "+680"
            },  
            {
                "country": "Palestinian State",
                "country_code": "PS",
                "dialing_code": "+970"
            },  
            {
                "country": "Panama",
                "country_code": "PA",
                "dialing_code": "+507"
            },  
            {
                "country": "Papua New Guinea",
                "country_code": "PG",
                "dialing_code": "+675"
            },  
            {
                "country": "Paraguay",
                "country_code": "PY",
                "dialing_code": "+595"
            },  
            {
                "country": "Peru",
                "country_code": "PE",
                "dialing_code": "+51"
            },  
            {
                "country": "Philippines",
                "country_code": "PH",
                "dialing_code": "+63"
            },  
            {
                "country": "Pitcairn Island",
                "country_code": "PN",
                "dialing_code": ""
            },  
            {
                "country": "Poland",
                "country_code": "PL",
                "dialing_code": "+48"
            },  
            {
                "country": "Portugal",
                "country_code": "PT",
                "dialing_code": "+351"
            },  
            {
                "country": "Puerto Rico",
                "country_code": "PR",
                "dialing_code": "+1-787 or +1-939"
            },  
            {
                "country": "Qatar, State",
                "country_code": "QA",
                "dialing_code": "+974"
            },  
            {
                "country": "Reunion",
                "country_code": "RE",
                "dialing_code": "+262"
            },  
            {
                "country": "Romania",
                "country_code": "RO",
                "dialing_code": "+40"
            },  
            {
                "country": "Russia - USSR",
                "country_code": "SU",
                "dialing_code": ""
            },  
            {
                "country": "Russian Federation",
                "country_code": "RU",
                "dialing_code": "+7"
            },  
            {
                "country": "Rwanda",
                "country_code": "RW",
                "dialing_code": "+250"
            },  
            {
                "country": "Saint Helena",
                "country_code": "SH",
                "dialing_code": "+290"
            },  
            {
                "country": "Saint Kitts and Nevis",
                "country_code": "KN",
                "dialing_code": "-868"
            },  
            {
                "country": "Saint Lucia",
                "country_code": "LC",
                "dialing_code": "-757"
            },  
            {
                "country": "Saint Pierre and Miquelon",
                "country_code": "PM",
                "dialing_code": "+508"
            },  
            {
                "country": "Saint Vincent and the Grenadines",
                "country_code": "VC",
                "dialing_code": "-783"
            },  
            {
                "country": "Samoa",
                "country_code": "WS",
                "dialing_code": "+685"
            },  
            {
                "country": "San Marino",
                "country_code": "SM",
                "dialing_code": "+378"
            },  
            {
                "country": "Sao Tome and Principe",
                "country_code": "ST",
                "dialing_code": "+239"
            },  
            {
                "country": "Saudi Arabia",
                "country_code": "SA",
                "dialing_code": "+966"
            },  
            {
                "country": "Serbia, Republic",
                "country_code": "RS",
                "dialing_code": ""
            },  
            {
                "country": "Senegal",
                "country_code": "SN",
                "dialing_code": "+221"
            },  
            {
                "country": "Seychelles",
                "country_code": "SC",
                "dialing_code": "+248"
            },  
            {
                "country": "Sierra Leone",
                "country_code": "SL",
                "dialing_code": "+232"
            },  
            {
                "country": "Singapore",
                "country_code": "SG",
                "dialing_code": "+65"
            },  
            {
                "country": "Slovakia",
                "country_code": "SK",
                "dialing_code": "+421"
            },  
            {
                "country": "Slovenia",
                "country_code": "SI",
                "dialing_code": "+386"
            },  
            {
                "country": "Solomon Islands",
                "country_code": "SB",
                "dialing_code": "+677"
            },  
            {
                "country": "Somalia",
                "country_code": "SO",
                "dialing_code": "+252"
            },  
            {
                "country": "South Africa",
                "country_code": "ZA",
                "dialing_code": "+27"
            },  
            {
                "country": "South Georgia and the South Sandwich Islands",
                "country_code": "GS",
                "dialing_code": ""
            },  
            {
                "country": "Spain",
                "country_code": "ES",
                "dialing_code": "+34"
            },  
            {
                "country": "Sri Lanka",
                "country_code": "LK",
                "dialing_code": "+94"
            },  
            {
                "country": "Sudan",
                "country_code": "SD",
                "dialing_code": "+249"
            },  
            {
                "country": "Suriname",
                "country_code": "SR",
                "dialing_code": "+597"
            },  
            {
                "country": "Svalbard",
                "country_code": "SJ",
                "dialing_code": ""
            },  
            {
                "country": "Swaziland, Kingdom",
                "country_code": "SZ",
                "dialing_code": "+268"
            },  
            {
                "country": "Sweden",
                "country_code": "SE",
                "dialing_code": "+46"
            },  
            {
                "country": "Switzerland",
                "country_code": "CH",
                "dialing_code": "+41"
            },  
            {
                "country": "Syria",
                "country_code": "SY",
                "dialing_code": "+963"
            },  
            {
                "country": "Taiwan",
                "country_code": "TW",
                "dialing_code": "+886"
            },  
            {
                "country": "Tajikistan",
                "country_code": "TJ",
                "dialing_code": "+992"
            },  
            {
                "country": "Tanzania, United Republic",
                "country_code": "TZ",
                "dialing_code": "+255"
            },  
            {
                "country": "Thailand",
                "country_code": "TH",
                "dialing_code": "+66"
            },  
            {
                "country": "Togo",
                "country_code": "TG",
                "dialing_code": ""
            },  
            {
                "country": "Tokelau",
                "country_code": "TK",
                "dialing_code": "+690"
            },  
            {
                "country": "Tonga, Kingdom",
                "country_code": "TO",
                "dialing_code": "+676"
            },  
            {
                "country": "Trinidad and Tobago",
                "country_code": "TT",
                "dialing_code": "-867"
            },  
            {
                "country": "Tromelin Island",
                "country_code": "TE",
                "dialing_code": ""
            },  
            {
                "country": "Tunisia",
                "country_code": "TN",
                "dialing_code": "+216"
            },  
            {
                "country": "Turkey",
                "country_code": "TR",
                "dialing_code": "+90"
            },  
            {
                "country": "Turkmenistan",
                "country_code": "TM",
                "dialing_code": "+993"
            },  
            {
                "country": "Turks and Caicos Islands",
                "country_code": "TC",
                "dialing_code": "-648"
            },  
            {
                "country": "Tuvalu",
                "country_code": "TV",
                "dialing_code": "+688"
            },  
            {
                "country": "Uganda, Republic",
                "country_code": "UG",
                "dialing_code": "+256"
            },  
            {
                "country": "Ukraine",
                "country_code": "UA",
                "dialing_code": "+380"
            },  
            {
                "country": "United Arab Emirates",
                "country_code": "AE",
                "dialing_code": "+971"
            },  
            {
                "country": "United Kingdom",
                "country_code": "GB",
                "dialing_code": "+44"
            },  
            {
                "country": "United States",
                "country_code": "US",
                "dialing_code": "+1"
            },  
            {
                "country": "United States Minor Outlying Islands",
                "country_code": "UM",
                "dialing_code": ""
            },  
            {
                "country": "Uruguay, Oriental Republic",
                "country_code": "UY",
                "dialing_code": "+598"
            },  
            {
                "country": "Uzbekistan",
                "country_code": "UZ",
                "dialing_code": "+998"
            },  
            {
                "country": "Vanuatu",
                "country_code": "VU",
                "dialing_code": "+678"
            },  
            {
                "country": "Vatican City State",
                "country_code": "VA",
                "dialing_code": "+418"
            },  
            {
                "country": "Venezuela",
                "country_code": "VE",
                "dialing_code": "+58"
            },  
            {
                "country": "Vietnam",
                "country_code": "VN",
                "dialing_code": "+84"
            },  
            {
                "country": "Virgin Islands, British",
                "country_code": "VI",
                "dialing_code": "-283"
            },  
            {
                "country": "Virgin Islands, United States",
                "country_code": "VQ",
                "dialing_code": "-339"
            },  
            {
                "country": "Wallis and Futuna Islands",
                "country_code": "WF",
                "dialing_code": "+681"
            },  
            {
                "country": "Western Sahara",
                "country_code": "EH",
                "dialing_code": ""
            },  
            {
                "country": "Yemen",
                "country_code": "YE",
                "dialing_code": "+967"
            },  
            {
                "country": "Yugoslavia",
                "country_code": "YU",
                "dialing_code": ""
            },  
            {
                "country": "Zaire",
                "country_code": "ZR",
                "dialing_code": ""
            },  
            {
                "country": "Zambia, Republic",
                "country_code": "ZM",
                "dialing_code": "+260"
            },  
            {
                "country": "Zimbabwe, Republic",
                "country_code": "ZW",
                "dialing_code": "+263"
            }]
        length = len(all_code)
        print(length)

        for i in range(0,length):
            code_data = all_code[i]
            print(code_data['country']," | ",code_data['country_code']," | ",code_data['dialing_code'])

            CountryCode.objects.create(country=code_data['country'],country_code=code_data['country_code'],dialing_code=code_data['dialing_code'])

        print("------------Process End--------------------")