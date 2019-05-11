module Main exposing (Item(..), Model, Msg(..), Package, Packages, decodePackage, getSearchResults, init, main, resultsDecoder, subscriptions, update, view)

import Browser
import DateFormat
import Html exposing (..)
import Html.Attributes as Attributes
import Html.Events exposing (..)
import Http
import Json.Decode as Decode
import Json.Decode.Extra as DExtra
import Json.Decode.Pipeline exposing (hardcoded, required)
import Time



-- MAIN


main =
    Browser.element
        { init = init
        , update = update
        , subscriptions = subscriptions
        , view = view
        }



-- MODEL


type alias Model =
    { packages : List Package
    }


init : () -> ( Model, Cmd Msg )
init _ =
    ( Model [], Cmd.none )


type Item
    = Grid
    | Source


type alias Packages =
    { packages : List Package }


type alias Package =
    { title : String
    , weight : Int
    , description : String
    , dateLastCommitted : Maybe Time.Posix
    , repoForks : Int
    , repoWatchers : Int
    , absoluteUrl : String
    , dateCreated : Time.Posix
    , dateModified : Time.Posix
    , itemType : Item
    }



-- UPDATE


type Msg
    = SearchInput String
    | GotResults (Result Http.Error Packages)


update : Msg -> Model -> ( Model, Cmd Msg )
update msg model =
    case msg of
        SearchInput query ->
            if query == "" then
                ( { model | packages = [] }, Cmd.none )

            else
                ( model, getSearchResults query )

        GotResults result ->
            case result of
                Ok data ->
                    ( { model | packages = data.packages }, Cmd.none )

                Err _ ->
                    ( model, Cmd.none )



-- SUBSCRIPTIONS


subscriptions : Model -> Sub Msg
subscriptions model =
    Sub.none



-- VIEW


dateFormater : Time.Zone -> Time.Posix -> String
dateFormater =
    DateFormat.format
        [ DateFormat.monthNameFull
        , DateFormat.text " "
        , DateFormat.dayOfMonthSuffix
        , DateFormat.text ", "
        , DateFormat.yearNumber
        ]


prettyDate : Time.Posix -> String
prettyDate time =
    dateFormater Time.utc time


resultRow : Package -> Html Msg
resultRow package =
    let
        description =
            case package.itemType of
                Source ->
                    "Package: " ++ package.description

                Grid ->
                    "Grid: " ++ package.description

        lastCommit =
            case package.dateLastCommitted of
                Just time ->
                    prettyDate time

                Nothing ->
                    "N/A"

        repoForks =
            case package.itemType of
                Source ->
                    String.fromInt package.repoForks

                Grid ->
                    "N/A"

        stars_ =
            case package.itemType of
                Source ->
                    String.fromInt package.repoWatchers

                Grid ->
                    "N/A"
    in
    tr []
        [ td [] [ text (String.fromInt package.weight) ]
        , td [] [ a [ Attributes.href package.absoluteUrl ] [ text package.title ] ]
        , td [] [ text description ]
        , td [] [ text lastCommit ]
        , td [] [ text repoForks ]
        , td [] [ text stars_ ]
        ]


resultsTable : Model -> List (Html Msg)
resultsTable model =
    if List.length model.packages == 0 then
        [ div [] [] ]

    else
        [ div [ Attributes.class "container" ]
            [ div [ Attributes.class "row" ]
                [ div [ Attributes.class "col-12" ]
                    [ table [ Attributes.class "table" ]
                        [ thead []
                            [ tr []
                                [ th [] [ text "Search Weight" ]
                                , th [] [ text "Package" ]
                                , th [] [ text "Description" ]
                                , th [] [ text "Last commit:" ]
                                , th [] [ text "Repo Forks" ]
                                , th [] [ text "Stars" ]
                                ]
                            ]
                        , tbody [] (List.map resultRow model.packages)
                        ]
                    ]
                ]
            ]
        ]


view : Model -> Html Msg
view model =
    div []
        ([ form [ Attributes.class "navbar-form pull-left hidden-xs" ]
            [ input
                [ Attributes.type_ "text"
                , Attributes.name "q"
                , Attributes.class "col-12 form-control"
                , Attributes.style "width" "240px;"
                , Attributes.id "search-2"
                , Attributes.placeholder "Search"
                , Attributes.autocomplete False
                , onInput SearchInput
                ]
                []
            ]
         ]
            ++ resultsTable model
        )



-- HTTP


getSearchResults : String -> Cmd Msg
getSearchResults query =
    Http.get
        { url = "/api/v4/search/?q=" ++ query
        , expect = Http.expectJson GotResults resultsDecoder
        }


resultsDecoder : Decode.Decoder Packages
resultsDecoder =
    Decode.succeed Packages
        |> required "entries" (Decode.list decodePackage)


decodePackage : Decode.Decoder Package
decodePackage =
    Decode.succeed Package
        |> required "title" Decode.string
        |> required "weight" Decode.int
        |> required "description" Decode.string
        |> DExtra.andMap (Decode.field "last_committed" (Decode.maybe DExtra.datetime))
        |> required "repo_forks" Decode.int
        |> required "repo_watchers" Decode.int
        |> required "absolute_url" Decode.string
        |> required "created" DExtra.datetime
        |> required "modified" DExtra.datetime
        |> required "item_type" item


item : Decode.Decoder Item
item =
    Decode.string
        |> Decode.andThen infoHelp


infoHelp : String -> Decode.Decoder Item
infoHelp item_type =
    case item_type of
        "package" ->
            packageDecoder

        "grid" ->
            gridDecoder

        _ ->
            Decode.fail <|
                "Trying to decode Package, but item_type "
                    ++ item_type
                    ++ " is not supported."


packageDecoder : Decode.Decoder Item
packageDecoder =
    Decode.succeed Source


gridDecoder : Decode.Decoder Item
gridDecoder =
    Decode.succeed Grid
