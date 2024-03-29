%define		_modname	http
%define		_fmodname	pecl_http
%define		_status		stable
%define		_sysconfdir	/etc/php4
%define		extensionsdir	%(php-config --extension-dir 2>/dev/null)
Summary:	%{_modname} - extended HTTP support
Summary(pl.UTF-8):	%{_modname} - rozszerzona obsługa protokołu HTTP
Name:		php4-pecl-%{_modname}
Version:	1.3.3
Release:	6
License:	BSD
Group:		Development/Languages/PHP
Source0:	http://pecl.php.net/get/%{_fmodname}-%{version}.tgz
# Source0-md5:	96c16435936eab288d5fdd5750e3f863
URL:		http://pecl.php.net/package/pecl_http/
BuildRequires:	php4-devel >= 3:4.3.0
BuildRequires:	rpmbuild(macros) >= 1.344
Requires:	php4-common >= 3:4.4.0-3
Obsoletes:	php-pear-%{_modname}
%{?requires_php_extension}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This HTTP extension aims to provide a convenient and powerful set of
functionality for one of PHPs major applications.

It eases handling of HTTP urls, dates, redirects, headers and
messages, provides means for negotiation of clients preferred language
and charset, as well as a convenient way to send any arbitrary data
with caching and resuming capabilities.

It provides powerful request functionality, if built with CURL
support. Parallel requests are available for PHP 5 and greater.

Currently implemented features include:
- Building absolute URIs
- RFC compliant HTTP redirects
- RFC compliant HTTP date handling
- Parsing of HTTP headers and messages
- Caching by "Last-Modified" and/or ETag (with 'on the fly' option for
  ETag generation from buffered output)
- Sending data/files/streams with (multiple) ranges support
- Negotiating user preferred language/charset
- Convenient request functions to HEAD/GET/POST if libcurl is
  available
- HTTP auth hooks (Basic)
- PHP5 classes: HttpUtil, HttpResponse, HttpRequest, HttpRequestPool,
  HttpMessage

In PECL status of this extension is: %{_status}.

%description -l pl.UTF-8
To rozszerzenie HTTP ma na celu dostarczenie wygodnego i potężnego
zestawu funkcjonalności do jednego z najważniejszych zastosowań PHP.

Ułatwia obsługę adresów HTTP, dat, przekierowań, nagłówków i
wiadmości, dostarcza sposób do negocjacji preferowanego języka i
strony kodowej klienta, jak również wygodnego sposobu wysyłania
dowolnego rodzaju danych z możliwością keszowania oraz wznawiania
transferów.

Rozszerzenie dostracza potężne możliwości zapytań, jeśli zbudowane
jest ze wsparciem dla CURL. Równoległe zapytania są dostępne od wersji
PHP 5.

Aktualnie zaimplementowane możliwości to między innymi:
- tworzenie bezwzględnych URI
- zgodne z RFC przekierowania HTTP
- zgodna z RFC obsługa daty HTTP
- przetwarzanie nagłówków i wiadomości HTTP
- buforowanie z użyciem "Last-Modified" i/lub ETagów (z opcję
  generowania "w locie" ETagów z buforowanego wyjścia)
- wysyłanie danych/plików/strumieni z obsługą (wielu) przedziałów
- negocjacja preferowanego przez użytkownika języka/zestawu znaków
- wygodne funkcje do żądań HEAD/GET/POST jeśli dostępna jest libcurl
- wywołania HTTP auth (Basic)
- klasy PHP5: HttpUtil, HttpResponse, HttpRequest, HttpRequestPool,
  HttpMessage

To rozszerzenie ma w PECL status: %{_status}.

%prep
%setup -q -c

%build
cd %{_fmodname}-%{version}
phpize
%configure
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sysconfdir}/conf.d,%{extensionsdir}}

install %{_fmodname}-%{version}/modules/%{_modname}.so $RPM_BUILD_ROOT%{extensionsdir}/%{_modname}.so
cat <<'EOF' > $RPM_BUILD_ROOT%{_sysconfdir}/conf.d/%{_modname}.ini
; Enable %{_modname} extension module
extension=%{_modname}.so
EOF

%clean
rm -rf $RPM_BUILD_ROOT

%post
%php4_webserver_restart

%postun
if [ "$1" = 0 ]; then
	%php4_webserver_restart
fi

%files
%defattr(644,root,root,755)
%doc %{_fmodname}-%{version}/{KnownIssues.txt,docs}
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/conf.d/%{_modname}.ini
%attr(755,root,root) %{extensionsdir}/%{_modname}.so
